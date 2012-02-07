from reflibrary.models import *
from django.contrib import admin


admin.site.register(Artist)
admin.site.register(Role)
admin.site.register(Genre)
admin.site.register(Rhythm)

class SoundTrackFeaturingInline(admin.TabularInline):
    model = SoundTrackFeaturing
    extra = 3
    list_display = ('artist', 'role')

class SoundTrackAdmin(admin.ModelAdmin):
    list_filter = ['style_type', 'rhythm_type']
    list_display = ('name', 'release_date', 'duration', 'style_type', 'rhythm_type')
    date_hierarchy = 'release_date'
    inlines = [SoundTrackFeaturingInline]
admin.site.register(SoundTrack, SoundTrackAdmin)

class RecordFeaturingInline(admin.TabularInline):
    model = RecordFeaturing
    extra = 3
    list_display = ('artist', 'role')

class RecordAdmin(admin.ModelAdmin):
    list_filter = ['category', 'medium']
    list_display = ('title', 'matrix_number', 'category', 'medium')
    inlines = [RecordFeaturingInline]
admin.site.register(Record, RecordAdmin)

class StyleAdmin(admin.ModelAdmin):
    list_filter = ['genre_type']
    list_display = ('name', 'genre_type')
admin.site.register(Style, StyleAdmin)

class RecordCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'number_of_disc')
admin.site.register(RecordCategory, RecordCategoryAdmin)

class MediumAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
admin.site.register(Medium, MediumAdmin)


