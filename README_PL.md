# python-for-android

**python-for-android (p4a)** to narzędzie deweloperskie, które pakuje aplikacje Pythona do 
plików binarnych, które mogą działać na urządzeniach Android.

## Co może generować

Narzędzie może generować:

* **[Android Package](https://en.wikipedia.org/wiki/Apk_(file_format))** (APK) - 
  pliki gotowe do lokalnej instalacji na urządzeniu, szczególnie do testowania. 
  Ten format jest używany przez wiele [sklepów z aplikacjami](https://en.wikipedia.org/wiki/List_of_Android_app_stores),
  ale nie przez [Google Play Store](https://play.google.com/store/).
  
* **[Android App Bundle](https://developer.android.com/guide/app-bundle/faq)** (AAB) - 
  pliki, które mogą być udostępniane w [Google Play Store](https://play.google.com/store/).
  
* **[Android Archive](https://developer.android.com/studio/projects/android-library)** (AAR) - 
  pliki, które mogą być użyte jako pakiety wielokrotnego użytku dla innych projektów.

## Wsparcie dla architektur

Narzędzie wspiera wiele architektur CPU.

## Wsparcie dla frameworków

Wspiera aplikacje opracowane przy użyciu [frameworka Kivy](http://kivy.org), ale zostało 
zaprojektowane tak, aby być elastycznym w kwestii bibliotek backendowych (poprzez "bootstraps"). 
Wspiera również [PySDL2](https://pypi.org/project/PySDL2/) oraz 
[WebView](https://developer.android.com/reference/android/webkit/WebView) z serwerem webowym Python.

## Zarządzanie zależnościami

Automatycznie wspiera zależności od większości czystych pakietów Pythona. Dla innych 
pakietów, w tym tych, które zależą od kodu C, musi zostać napisany specjalny "recipe" 
(przepis), aby wspierać kompilację krzyżową. python-for-android zawiera wbudowane przepisy 
dla wielu najpopularniejszych bibliotek (np. numpy i sqlalchemy).

## Jak to działa

python-for-android działa poprzez kompilację krzyżową interpretera Pythona i jego 
zależności dla urządzeń Android, a następnie pakuje je z kodem pythonowym aplikacji 
i jej zależnościami. Kod Pythona jest następnie interpretowany na urządzeniu Android.

## Rekomendowane użycie

Zaleca się używanie python-for-android poprzez 
[Buildozer](https://buildozer.readthedocs.io/), który zapewnia prawidłowe 
wstępne zainstalowanie zależności i centralizuje konfigurację. Jednak 
python-for-android nie jest ograniczone tylko do użycia z Buildozer.

## Dokumentacja

Więcej informacji jest dostępnych w 
[dokumentacji online](https://python-for-android.readthedocs.io) wraz z 
[przewodnikiem szybkiego startu](https://python-for-android.readthedocs.io/en/latest/quickstart.html).

python-for-android jest zarządzane przez [zespół Kivy](https://kivy.org).

## Wsparcie

Czy masz problemy z używaniem python-for-android lub którymkolwiek z powiązanych projektów 
w ekosystemie Kivy? Czy jest jakiś błąd, którego nie rozumiesz? Próbujesz dowiedzieć się, 
jak go używać? Mamy wolontariuszy, którzy mogą pomóc!

Najlepsze kanały, aby się z nami skontaktować w sprawie wsparcia, są wymienione w najnowszym 
dokumencie [Skontaktuj się z nami](https://github.com/kivy/python-for-android/blob/master/CONTACT.md).

## Kod postępowania

W celu wspierania otwartej i przyjaznej społeczności, my jako 
współtwórcy i opiekunowie musimy zapewnić, że uczestnictwo w naszym projekcie i 
naszych siostrzanych projektach jest wolne od nękania i stanowi pozytywne doświadczenie dla wszystkich. 
Istotne jest, aby wszelkie interakcje były prowadzone w sposób wyrażający szacunek, 
otwartość umysłu i wdzięczność.

Zapoznaj się z najnowszym [Kodeksem postępowania](https://github.com/kivy/python-for-android/blob/master/CODE_OF_CONDUCT.md).

## Współtwórcy

Ten projekt istnieje dzięki 
[wszystkim osobom, które wnoszą swój wkład](https://github.com/kivy/python-for-android/graphs/contributors).
[[Zostań współtwórcą](CONTRIBUTING.md)].

## Sponsorzy i darczyńcy

Dziękujemy [wszystkim naszym darczyńcom](https://opencollective.com/kivy)! 
🙏 [[Zostań darczyńcą](https://opencollective.com/kivy#backer)]

Specjalne podziękowania dla 
[wszystkich naszych sponsorów, obecnych i przeszłych](https://opencollective.com/kivy).
Wesprzyj ten projekt, 
[[stając się sponsorem](https://opencollective.com/kivy#sponsor)].
