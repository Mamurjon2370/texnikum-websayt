from .models import SiteSettings, Program


def site_globals(request):
    return {
        "site": SiteSettings.get(),
        "nav_programs": Program.objects.filter(is_active=True)[:8],
    }
