from cloudinary.models import CloudinaryField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from tpm.models import BaseModel


class EducationalSystem(BaseModel):
    class Meta:
        verbose_name = _("Educational System")
        verbose_name_plural = _("Educational Systems")

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Faculty(BaseModel):
    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")

    name = models.CharField(max_length=30)

    educational_system = models.ForeignKey(EducationalSystem, on_delete=models.CASCADE, related_name="faculties")

    def __str__(self):
        return self.name


class Major(BaseModel):
    class Meta:
        verbose_name = _("Major")
        verbose_name_plural = _("Majors")

    name = models.CharField(max_length=30)

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="majors")

    def __str__(self):
        return self.name


class AcademicYear(BaseModel):
    class Meta:
        verbose_name = _("Academic Year")
        verbose_name_plural = _("Academic Years")

    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Class(BaseModel):
    class Meta:
        verbose_name = _("Class")
        verbose_name_plural = _("Classes")

    name = models.CharField(max_length=20)

    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name="classes")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="classes")

    def __str__(self):
        return self.name


class Semester(BaseModel):
    class Meta:
        verbose_name = _("Semester")
        verbose_name_plural = _("Semesters")

    name = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()

    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="semesters")

    def __str__(self):
        return self.name


class Criterion(BaseModel):
    class Meta:
        verbose_name = _("Criterion")
        verbose_name_plural = _("Criterions")

    name = models.CharField(max_length=20)
    max_point = models.SmallIntegerField()
    description = CKEditor5Field("Text", config_name="extends")

    def __str__(self):
        return self.name


class TrainingPoint(BaseModel):
    class Meta:
        verbose_name = _("Training Point")
        verbose_name_plural = _("Training Points")

    point = models.SmallIntegerField()

    # Thuộc học kỳ nào?
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="points")
    # Thuộc tiêu chí rèn luyện nào?
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE, related_name="points")
    # Của sinh viên nào?
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, related_name="points")

    def __str__(self):
        return f"{self.student.code} - {self.point} - {self.criterion} - {self.semester}"


class Activity(BaseModel):
    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    class Type(models.TextChoices):
        ONLINE = "Onl", _("Online")
        OFFLINE = "Off", _("Offline")

    # Hình thức tổ chức
    organizational_form = models.CharField(max_length=3, choices=Type, default=Type.OFFLINE)

    name = models.CharField(max_length=20)
    participant = models.CharField(max_length=20)  # Đối tượng tham gia
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    point = models.SmallIntegerField()  # Điểm được cộng
    description = CKEditor5Field("Text", config_name="extends")

    # Danh sách sinh viên tham gia
    list_of_participants = models.ManyToManyField("users.Student", related_name="activities", through="Participation")

    # Thuộc khoa nào?
    faculty = models.ForeignKey("schools.Faculty", on_delete=models.CASCADE, related_name="activities")
    # Thuộc học kỳ nào?
    semester = models.ForeignKey("schools.Semester", on_delete=models.CASCADE, related_name="activities")
    # Người tạo là ai?
    created_by_type = models.ForeignKey("contenttypes.ContentType", on_delete=models.CASCADE, related_name="activities")
    created_by_id = models.PositiveIntegerField()
    created_by = GenericForeignKey("created_by_type", "created_by_id")
    # Cộng điểm rèn luyện điều mấy?
    criterion = models.ForeignKey("schools.Criterion", null=True, on_delete=models.SET_NULL, related_name="activities")

    def __str__(self):
        return self.name


class Participation(BaseModel):
    class Meta:
        verbose_name = _("participation")
        verbose_name_plural = _("participations")
        unique_together = ("student", "activity")  # Sinh viên chỉ đăng ký tham gia hoạt động một lần

    is_attendance = models.BooleanField(default=False)
    is_point_added = models.BooleanField(default=False)

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="participation")
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, related_name="participation")

    def __str__(self):
        return f"{self.student.code} - {self.activity}"

    def save(self, *args, **kwargs):
        if self.is_attendance and not self.is_point_added:
            self.student.points.add(TrainingPoint.objects.create(
                point=self.activity.point,
                semester=self.activity.semester,
                criterion=self.activity.criterion,
                student=self.student
            ))
            self.is_point_added = True
        super().save(*args, **kwargs)


class DeficiencyReport(BaseModel):
    class Meta:
        verbose_name = _("Deficiency Report")
        verbose_name_plural = _("Deficiency Reports")
        unique_together = ("student", "activity")

    is_resolved = models.BooleanField(default=False)  # Đã giải quyết chưa?
    image = CloudinaryField(null=True, blank=True)  # Hình ảnh minh chứng
    content = CKEditor5Field("Text", config_name="extends", null=True, blank=True)

    # Của sinh viên nào?
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, related_name="deficiency_reports")
    # Thuộc hoạt động nào?
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="deficiency_reports")

    def __str__(self):
        return f"{self.student.code} - {self.activity}"
