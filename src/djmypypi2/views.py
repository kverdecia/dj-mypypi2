"Views for a python package index"
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, permission_required

from . import models
from . import decorators


class PackageListView(ListView):
    "Python package index view"
    template_name = 'djmypypi2/package-list.html'
    queryset = models.Package.objects.order_by('name')


class PackageDetailView(DetailView):
    "Python package view"
    template_name = 'djmypypi2/package-detail.html'
    model = models.Package
    slug_field = 'name'
    slug_url_kwarg = 'package_name'


def download_package(request, archive_name) -> FileResponse:
    "Handler to download a package"
    version = get_object_or_404(models.Version, archive_name=archive_name)
    version.archive.open()
    return FileResponse(version.archive, as_attachment=True, filename=archive_name)


@csrf_exempt
@decorators.basic_authentication
@login_required
@permission_required('djmypypi2.add_package', raise_exception=True)
def upload_package(request):
    "Handle uploading a package."
    package_file = request.FILES['content']
    # validates the archive does not exist
    if models.Version.version_archive_exist(package_file.name):
        return HttpResponseBadRequest("This package archive already exist: {}".format(
            package_file.name))
    # get or create the package
    try:
        package = models.Package.objects.get(name=request.POST['name'])
        if package.user.pk != request.user.pk:
            return HttpResponseForbidden("You are not the owner of this package")
    except models.Package.DoesNotExist:
        package = models.Package()
        package.name = request.POST['name']
        package.user = request.user

    version = models.Version(package=package)

    package.version = version.version = request.POST['version']
    package.author = version.author = request.POST.get('author', '')
    package.author_email = version.author_email = request.POST.get('author_email', '')
    package.maintainer = version.maintainer = request.POST.get('maintainer', '')
    package.maintainer_email = version.maintainer_email = request.POST.get('maintainer_email', '')
    package.summary = version.summary = request.POST.get('summary', '')
    package.description = version.description = request.POST.get('description', '')
    package.home_page = version.home_page = request.POST.get('home_page', '')
    package.license = version.license = request.POST.get('license', '')
    package.classifiers = version.classifiers = "\n".join(request.POST.getlist('classifiers', []))
    version.md5_digest = request.POST.get('md5_digest', '')
    version.archive_name = package_file.name

    import rich
    rich.print(request.POST)

    package.save()
    version.save()

    version.archive.save(package_file.name, package_file, save=True)

    return HttpResponse("ok")
