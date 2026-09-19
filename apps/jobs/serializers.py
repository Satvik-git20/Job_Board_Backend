from rest_framework import serializers
from .models import Job, SavedJob
from apps.accounts.serializers import EmployerProfileSerializer

class JobSerializer(serializers.ModelSerializer):
    employer = EmployerProfileSerializer(read_only=True)
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            'id', 'employer', 'title', 'description', 'location',
            'salary_min', 'salary_max', 'experience_required',
            'job_type', 'skills_required', 'openings',
            'application_deadline', 'status', 'is_saved',
            'created_at', 'updated_at'
        )

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'candidate':
            if hasattr(request.user, 'candidate_profile'):
                return SavedJob.objects.filter(candidate=request.user.candidate_profile, job=obj).exists()
        return False

class JobCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'title', 'description', 'location',
            'salary_min', 'salary_max', 'experience_required',
            'job_type', 'skills_required', 'openings',
            'application_deadline', 'status'
        )

    def validate(self, attrs):
        salary_min = attrs.get('salary_min')
        salary_max = attrs.get('salary_max')
        if salary_min is not None and salary_max is not None and salary_min > salary_max:
            raise serializers.ValidationError({"salary_min": "Minimum salary cannot be greater than maximum salary."})
        return attrs

class SavedJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.filter(status='active'),
        write_only=True,
        source='job'
    )

    class Meta:
        model = SavedJob
        fields = ('id', 'job', 'job_id', 'saved_at')

    def create(self, validated_data):
        candidate_profile = self.context['request'].user.candidate_profile
        job = validated_data['job']
        saved_job, created = SavedJob.objects.get_or_create(candidate=candidate_profile, job=job)
        return saved_job
