
rmdir /s /q build
cmake -H. -Bbuild -G "Visual Studio 15 2017 Win64"
cmake --build build