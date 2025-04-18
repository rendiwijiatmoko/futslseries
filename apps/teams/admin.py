from django.contrib import admin
from .models import Region, Team, Player

# Membuat Inline untuk Player, agar bisa ditambahkan langsung di halaman Team admin
class PlayerInline(admin.TabularInline):  # Bisa juga menggunakan admin.StackedInline
    model = Player
    extra = 1  # Menambahkan 1 form kosong untuk menambah pemain baru
    fields = ['name', 'position', 'jersey_number', 'guardian_name', 'is_captain']
    # Jika ingin menampilkan foto dan dokumen pendukung, tambahkan field-nya
    # fields = ['name', 'position', 'jersey_number', 'guardian_name', 'photo', 'supporting_document', 'is_captain']

# Mengatur admin panel untuk Region
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# Mengatur admin panel untuk Team dengan inline Player
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'region', 'category', 'status', 'is_main')
    search_fields = ('school_name', 'school_nickname')
    list_editable = ('is_main',)
    list_filter = ('region', 'category', 'status')
    inlines = [PlayerInline]

# Mengatur admin panel untuk Player
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'position', 'jersey_number', 'is_captain']
    search_fields = ['name', 'team__school_name', 'position']


# from django.contrib import admin
# from .models import Region, Team, Player

# @admin.register(Region)
# class RegionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')

# class PlayerInline(admin.TabularInline):
#     model = Player
#     extra = 0

# @admin.register(Team)
# class TeamAdmin(admin.ModelAdmin):
#     list_display = ('school_name', 'region', 'category', 'status')
#     search_fields = ('school_name', 'school_nickname')
#     list_filter = ('region', 'category', 'status')
#     inlines = [PlayerInline]
