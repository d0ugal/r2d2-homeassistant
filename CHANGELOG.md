# Changelog

## [1.2.0](https://github.com/d0ugal/r2d2-homeassistant/compare/v1.1.0...v1.2.0) (2026-04-05)


### Features

* add button, select, and light entity platforms ([2d36b15](https://github.com/d0ugal/r2d2-homeassistant/commit/2d36b15f2b8b41cd25f8b86baa98a8ada01954ed))

## [1.1.0](https://github.com/d0ugal/r2d2-homeassistant/compare/v1.0.0...v1.1.0) (2026-04-04)


### Features

* add all 16 named character sounds, extra/animation bytes, and icon ([69b4add](https://github.com/d0ugal/r2d2-homeassistant/commit/69b4add43ef4cb40c47078a213671720c551c8b1))
* head slider for fine-grained rotation (raw byte 4–36) ([20d73af](https://github.com/d0ugal/r2d2-homeassistant/commit/20d73af363ad9ceb59b5fcffe2759a7a65dc4e7c))
* initial R2D2 Home Assistant integration ([c253e75](https://github.com/d0ugal/r2d2-homeassistant/commit/c253e75694ae1101431de102d212b21f9fa5b92b))


### Bug Fixes

* correct LED byte positions ([8]/[9] not [10]/[11]), add 8 directions ([9ecf63d](https://github.com/d0ugal/r2d2-homeassistant/commit/9ecf63dc0f6910148f1f9459627cc5ffd0c047af))
* correct sound-to-character mapping (1=C3PO...8=Trooper, 9=Vader, 10=Yoda) ([ec46fca](https://github.com/d0ugal/r2d2-homeassistant/commit/ec46fca53b63679a3e0a7d856612052b2a7dc803))
* match R2D2 device name with null-byte padding ([e5c6eee](https://github.com/d0ugal/r2d2-homeassistant/commit/e5c6eeecadcbc7596db855aaa42bf601a70b98da))
* replace character sound pairs with correct Sfx1-Sfx10 byte mapping ([b37d8a7](https://github.com/d0ugal/r2d2-homeassistant/commit/b37d8a7169896b9274f18ee8d2cecc57542c62d6))
* resolve CI failures (manifest key order, missing imports, EN dashes, type errors) ([0dd3f46](https://github.com/d0ugal/r2d2-homeassistant/commit/0dd3f468c7825440522cec63e0c5a30c31757f32))
* ruff format, HACS brand assets, pyright suppressions, add Makefile ([2171200](https://github.com/d0ugal/r2d2-homeassistant/commit/21712009d5f64c9b5dad7dd7f7591ef7844498be))


### Documentation

* realistic automation examples, fix sound count (10 not 16) ([7bda7e3](https://github.com/d0ugal/r2d2-homeassistant/commit/7bda7e3b0f0904db5660f94607b0645b8d173be6))
* update README with all 8 directions, 16 sounds, BLE protocol notes ([72ce76a](https://github.com/d0ugal/r2d2-homeassistant/commit/72ce76a7dc09017433ec79ddb8eec75cff64477e))
