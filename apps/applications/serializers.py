from rest_framework import serializers
from .models import Resume, JobApplication, ApplicationStatus
from apps.jobs.models import Job, JobStatus
from apps.jobs.serializers import JobSerializer
from apps.accounts.serializers import CandidateProfileSerializer

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('id', 'resume_file', 'file_type', 'uploaded_at')
        read_only_fields = ('id', 'file_type', 'uploaded_at')

    def create(self, validated_data):
        candidate_profile = self.context['request'].user.candidate_profile
        resume_file = validated_data['resume_file']
        return Resume.objects.create(
            candidate=candidate_profile,
            resume_file=resume_file,
            file_type='application/pdf'
        )

class JobApplicationSerializer(serializers.ModelSerializer):
    candidate = CandidateProfileSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    resume = ResumeSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = ('id', 'candidate', 'job', 'resume', 'status', 'applied_at', 'updated_at')

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.filter(status=JobStatus.ACTIVE),
        write_only=True,
        source='job'
    )
    resume_id = serializers.PrimaryKeyRelatedField(
        queryset=Resume.objects.all(),
        write_only=True,
        source='resume'
    )

    class Meta:
        model = JobApplication
        fields = ('id', 'job_id', 'resume_id', 'status', 'applied_at')
        read_only_fields = ('id', 'status', 'applied_at')

    def validate(self, attrs):
        user = self.context['request'].user
        candidate = user.candidate_profile
        job = attrs['job']
        resume = attrs['resume']

        # Ensure resume belongs to the candidate
        if resume.candidate != candidate:
            raise serializers.ValidationError({"resume_id": "Selected resume does not belong to your candidate profile."})

        # Ensure candidate has not applied twice
        if JobApplication.objects.filter(candidate=candidate, job=job).exists():
            raise serializers.ValidationError({"job_id": "You have already applied for this job."})

        return attrs

    def create(self, validated_data):
        candidate = self.context['request'].user.candidate_profile
        return JobApplication.objects.create(
            candidate=candidate,
            job=validated_data['job'],
            resume=validated_data['resume']
        )

class JobApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=ApplicationStatus.choices)

    class Meta:
        model = JobApplication
        fields = ('status',)
