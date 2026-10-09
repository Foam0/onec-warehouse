# Attribution and modifications

Application BSL modules, business rules, tests, documentation and scripts:
Copyright (c) 2026 Egor Golikov. LGPL-3.0-or-later.

The XML metadata scaffolding is adapted from test fixtures maintained by the
1c-syntax contributors (LGPL-3.0):

- https://github.com/1c-syntax/bsl-language-server/tree/0e43799635bfad9ad70c006415b6eb3de4c07f89/src/test/resources/metadata/designer
- https://github.com/1c-syntax/mdclasses/tree/2031e0bc9f714d41879aa28fa5ed3cc12a3a2cc9/src/test/resources/ext/designer/mdclasses/src/cf
- https://github.com/1c-syntax/mdclasses/tree/2031e0bc9f714d41879aa28fa5ed3cc12a3a2cc9/src/test/resources/ext/designer/mdclasses_3_25/src/cf

Modified on 2026-10-09: configuration identities, object composition, object names,
UUIDs and generated type identifiers, field types and precision, posting settings,
form attributes and commands, register dimensions/resources, role permissions,
queries and report settings. Fixture application logic was not copied.

The complete preferred source is included under src/; tests and scripts are included.
LICENSE contains LGPLv3 and COPYING contains GPLv3, incorporated by LGPLv3.
1C:Enterprise is a separate proprietary runtime, not included in this repository.
OneScript and BSL Language Server binaries are downloaded by CI, not redistributed here.
