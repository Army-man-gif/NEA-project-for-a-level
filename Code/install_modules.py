import subprocess
def install_modules(module_list):
    for module in module_list:
        try:
            subprocess.check_call(['pip', 'install', module])
            print(f"Successfully installed {module}")
        except subprocess.CalledProcessError:
            print(f"Error installing {module}")
            
modules_to_install = [
        'sqlite4',
        '1OS',
        'Everything-Tkinter',
        'requests',
        'bs4',
        'urllib3',
        'pillow',
        'extended-maths',
        'random2',
        'python-time',
        'w2re',
        'continuous-threading',
        'gspread',
        'oauth2client',
        'google_api',
        'google-api-python-client',
        'tkcalendar',
        'matplotlib',
        'mplcursors',
        'scikit-image',
        'imageio',
        'numpy',
]
install_modules(modules_to_install)
