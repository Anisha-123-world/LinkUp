from django.contrib import admin
from .models import CustomUser,Skill,UserSkill,SwapRequest,Feedback

admin.site.register(CustomUser)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(SwapRequest)
admin.site.register(Feedback)
admin.site.site_header = "Odoo Hackathon Admin Panel"
admin.site.site_title = "Odoo Hackathon"
admin.site.index_title = "Welcome to the Admin Dashboard"

