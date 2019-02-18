#!/bin/bash
i686-w64-mingw32-gcc agent.cpp -o agent.exe -s -lws2_32 -Wno-write-strings -fno-exceptions -fmerge-all-constants -static-libstdc++ -static-libgcc -fpermissive
