import sys
try:
    from d51.django.virtualenv.test_runner import run_tests
except ImportError:
    print "Please install d51.django.virtualenv.test_runner to run these tests"

def setUp():
    from django.conf.urls.defaults import patterns, include, handler500, handler404
    sys.modules[setUp.__module__].handler500 = handler500
    sys.modules[setUp.__module__].handler404 = handler404
    sys.modules[setUp.__module__].urlpatterns = patterns('',
    )


def main():
    settings = {
        "INSTALLED_APPS": (
            "d51.django.apps.twitter",
        ),
        'ROOT_URLCONF': '__main__',
    }
    run_tests(settings, 'twitter')

if __name__ == '__main__':
    main()
