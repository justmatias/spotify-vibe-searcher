# CHANGELOG


## v0.8.0 (2026-01-06)

### Bug Fixes

- **config**: Add `all_genre_names` property for unique genre aggregation, standardize `spotify_url`
  output,
  ([`a091ba0`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/a091ba0d2fec0a0ca4f9a91f84cd75ee1bbedb1e))

### Chores

- **config**: Disable pylint too-many-locals warning
  ([`5aae8a2`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/5aae8a221b75f7e80b932b998d897aa82fb732bc))

- **config**: Rename project module
  ([`9fc9456`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/9fc94567e3aac1cf643d96c3068f27c683ad89f8))

- **config**: Update project description
  ([`3d50ce5`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/3d50ce5012b247fe78733020eb18e7c2b2174aff))

- **docs**: Update docs
  ([`aff30f2`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/aff30f2e782b1a836a8dbb8f1eb42260fcfc5281))

- **docs**: Update readme
  ([`ac3c526`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/ac3c52667c7a134023e35af62d830ab985796028))

- **docs**: Update readme
  ([`bd1f11d`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/bd1f11d98d77880c4950ee7d75a6a36f8590e6b8))

- **docs**: Update readme
  ([`a91ab66`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/a91ab663d8c5a7a6965c9f7a4a856bab24d77a5a))

### Features

- **config**: Enrich artist genres during library sync and add debug logging for track storage and
  analysis prompts
  ([`1a19af4`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/1a19af4c1b74374184cafa3b83f9d70e59695855))

- **config**: Introduce a UI button to clear the database
  ([`67fc911`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/67fc911e1bf276a2c68d5a868116d038619e3e92))

### Refactoring

- **config**: Remove early exit and use list comprehension with `get` for artist enrichment
  ([`7ddb164`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/7ddb164ef1b2e51ac8f773650042d7cd6055a2ae))


## v0.7.0 (2026-01-03)

### Bug Fixes

- **config**: Inject LLM client into SearchService
  ([`924224b`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/924224ba93e33730dd2934f16946f224ca9da3df))

### Features

- **config**: Add query refinement
  ([`a385437`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/a385437e2f15708fe8eee6d3dffe9bc0c326ef7e))


## v0.6.0 (2026-01-02)

### Bug Fixes

- **test**: Add vcr marker to track exists test
  ([`cb11119`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/cb111195b06797970a7f74aedfd5a1cf45010996))

- **ui**: Replace `use_container_width=True` with `width='stretch'` in UI components.
  ([`68c4b7a`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/68c4b7aa963cfe602e055bd7a53bf865533fcd42))


## v0.5.0 (2026-01-02)

### Bug Fixes

- **test**: Add tests for `count_tracks` and `get_all_tracks` to the vectordb repository
  ([`5b63da2`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/5b63da2c3ccf01b73df9f7ff895f5d4c610d15d0))

- **test**: Fix lint issues
  ([`5d7f234`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/5d7f2348fbd7b9bed363c9ce9e6148fb5492b2eb))

### Chores

- **docs**: Overhaul README with detailed features, architecture, quick start, and usage
  instructions
  ([`e5c00ef`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/e5c00ef78ac586c075b235c0eb93dc872684baca))

### Features

- **config**: Skip existing tracks during library synchronization to prevent re-indexing
  ([`9c26745`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/9c26745f0a3271ec82b6173d1fd6c207ba542552))

- **ui**: Introduce a library view to display indexed tracks
  ([`58d89cf`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/58d89cf6889375caa6fcbdaa40491662bde3788d))


## v0.4.1 (2026-01-02)

### Bug Fixes

- **config**: Remove column layout for search button and results slider
  ([`6d8bc15`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/6d8bc15700348f4e01f7482c92f92cb93b467135))


## v0.4.0 (2026-01-02)

### Bug Fixes

- **config**: Enhance application observability with detailed logging across services and clients
  ([`0be3c10`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/0be3c10f9bdb2b66e0c9b4afb4cddc860079451c))

- **config**: Remove `access_token` from search UI component and adjust
  `SearchResult.similarity_score` definition.
  ([`4452bd4`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/4452bd44752bfaa19a9bd88117f15546e84a6ece))

- **test**: Add unit tests and fixtures for the VectorDB repository
  ([`c0fea7a`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/c0fea7a26d8af3eed677c9a0996df13900237109))

- **test**: Add unit tests for TrackAnalysisService, including fixtures and VCR cassettes
  ([`0e320f7`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/0e320f709eb290cf82d7f94ca2cef89e3c557880))

- **test**: Enhace database track deletion tests with VCR cassettes
  ([`b1357a5`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/b1357a569f705bc3d8d318d2f672156bc7ba9059))

- **test**: Improve vector database test isolation in tests
  ([`3c4d437`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/3c4d43767c378b1f539f28f3e2a912f10ff9b78c))

### Chores

- **config**: Remove warning log when Genius client fails to find lyrics.
  ([`90e3eb3`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/90e3eb31d9a7a4b647d28df60f9cc4b8bd0657d1))

- **config**: Update pre-commit hooks
  ([`898ec2b`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/898ec2b2bd25cfff4690513bf7cdf4609e6a8639))

### Features

- **config**: Add semantic vibe search functionality
  ([`a821fa1`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/a821fa179c8039886072e73eb4b5ef1bd6a05d4f))

- **config**: Implement search by vibe functionality with new service, domain models, UI component,
  and comprehensive tests.
  ([`654f43b`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/654f43b6dd8867f7efd3c3822e16196105c7d99b))

### Refactoring

- **config**: Move imports to module scope, adjust test track data, and add pylint disable to
  conftest files.
  ([`9ca7e58`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/9ca7e58a2440bc01607910522103b3e13ea00bb1))


## v0.3.0 (2025-12-29)

### Bug Fixes

- **config**: Declare sub-containers using `providers.Container` for lazy loading.
  ([`a8b9cea`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/a8b9ceaa9df72902b47dae733981c4120c52119c))

- **test**: Add LLM client unit tests with VCR integration and update LLM base URL
  ([`4ab0fb9`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/4ab0fb9c23c8de95d7e31b0ac520083a193ff7a7))

- **test**: Implement tests for the LibrarySyncService and dependency injection container
  ([`1bf5272`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/1bf527294aede4f9662f22370490e61d30424ac8))

### Chores

- **config**: Fix lint issues
  ([`0f32ef9`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/0f32ef9535732d58298ad1d866db566a0df2e1c8))

- **config**: Remove docstring from `injections` container.
  ([`46bec22`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/46bec22eb5ef02c0d556cdee5787036f84c7972b))

- **config**: Update requirements.txt
  ([`1836612`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/1836612984d1e3994d705f4e9d047bfa3844a8c7))

- **config**: Update requirements.txt
  ([`50f44ff`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/50f44ff897b5ca9c2a0095d01640c9c555f17079))

- **config**: Update requirements.txt
  ([`baa41a2`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/baa41a2ea258fc8f4e1bfc6f31f20a71ab1c0cc6))

### Features

- **config**: Add LLM client, VectorDB repository, and track analysis service
  ([`a5b13a8`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/a5b13a8f626feac4b1e5506002cbaa08afca880d))

- **config**: Implement library synchronization with track enrichment and dependency injection for
  services and infrastructure
  ([`7172b12`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/7172b129b00994eacf1eb036db5261828be75e65))

- **config**: Integrate Ollama for track analysis and embedding, add VCR test cassettes, and adjust
  VCR and logging configurations.
  ([`a9b6636`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/a9b6636274349160b7c9d9645ac866b2f107bfc0))

### Refactoring

- **config**: Update DI container instantiation to directly create sub-containers and pass
  dependencies.
  ([`aaffc00`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/aaffc001b6e0162fc6a1e8f4448ecf6a3da69eb1))

- **test**: Consolidate Polyfactory fixtures into a new central plugin and remove them from
  individual conftest files
  ([`ca84eea`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/ca84eeaff6938bfa45e8632a9603f088093953da))


## v0.2.0 (2025-12-29)

### Chores

- **config**: Update pyproject.toml
  ([`50f1d6c`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/50f1d6c4fc41c9995e5fb890dbd701cb8f69e37f))

- **deps**: Bump actions/checkout from 4 to 6
  ([`1a9295d`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/1a9295d8778a2690d780bb7884aa4d7e10956392))

Bumps [actions/checkout](https://github.com/actions/checkout) from 4 to 6. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/actions/checkout/compare/v4...v6)

--- updated-dependencies: - dependency-name: actions/checkout dependency-version: '6'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump actions/setup-python from 5 to 6
  ([`676e247`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/676e2472835f7e287c8e3432ca0c13a9c69189cc))

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 5 to 6. - [Release
  notes](https://github.com/actions/setup-python/releases) -
  [Commits](https://github.com/actions/setup-python/compare/v5...v6)

--- updated-dependencies: - dependency-name: actions/setup-python dependency-version: '6'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump peter-evans/create-pull-request from 7 to 8
  ([`720c37c`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/720c37c9ac569e64cb6552296ccad5234ea7791a))

Bumps [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request) from 7
  to 8. - [Release notes](https://github.com/peter-evans/create-pull-request/releases) -
  [Commits](https://github.com/peter-evans/create-pull-request/compare/v7...v8)

--- updated-dependencies: - dependency-name: peter-evans/create-pull-request dependency-version: '8'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

### Features

- **test**: Add unit tests for Spotify domain models and authentication manager, and introduce
  polyfactory dependency
  ([`d943b71`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/d943b71ac24d460cff0b3fbb391c617f7b526cbe))


## v0.1.1 (2025-12-29)

### Bug Fixes

- **test**: Initialize app settings with test credentials
  ([`7f26d8c`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/7f26d8cecf7b6baf2fa99ef818958e0ce99fb8b1))

### Chores

- **config**: Adjust type ignore comment in Spotify client
  ([`2414b94`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/2414b9468cbf3d81cced656ce962f775c1ef67f9))


## v0.1.0 (2025-12-29)

### Bug Fixes

- **config**: Fix spotify client instantiation
  ([`01eca70`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/01eca703a624d0d8f510055811c2a314f16140e9))

### Chores

- **config**: Add GitHub Actions for CI, Dependabot, pre-commit autoupdate
  ([`d367a94`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/d367a943513af9fea7e31c2ff7c3d692c73e45dd))

- **config**: Add pre-commit configuration.
  ([`f2719cb`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/f2719cb23aabdddfce68860da4fad320b6ec4cfd))

- **config**: Add project versioning
  ([`15052fe`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/15052fee5329f2183dd8e42feda5ff32361bafd8))

- **config**: Add security pre-commit hooks
  ([`9d3111d`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/9d3111d1210af48ee5555cb8318ad0757aee20af))

- **config**: Dynamically fetch package version
  ([`a3e1569`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/a3e1569ebf1a3e0d6a0f2e91bf90d9ba51890209))

- **config**: Fix lint issues
  ([`6053279`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/6053279998166bc12318b601b28faa71b39a538c))

- **docs**: Add README.md
  ([`ffca9d2`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/ffca9d2e3a6d6d4c8b4bf3084f9b3de749b9761a))

- **docs**: Update .env.sample
  ([`01fb758`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/01fb7589c59ae8d639886f957a203894caf3f8ee))

- **docs**: Update implementation plan
  ([`af09cf3`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/af09cf310f10bf22f7ebd414435609dd081ce415))

### Features

- **config**: Add Genius API integration, new Spotify domain models, and refactor settings to use
  uppercase naming conventions.
  ([`ec2df90`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/ec2df90e4905bb420ba4fd7d7d720ad2a6a33f0c))

- **config**: Add Spotify authentication, API client, and user domain model, and refactor UI to use
  new infrastructure
  ([`7a33c38`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/7a33c385d3f30f25554a4faaec71fb1021566da9))

- **config**: Establish initial project structure, core modules, UI, and dependency management
  ([`2ce9a8e`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/2ce9a8e126836ea4a1394db6fa21158e68fd010c))

- **config**: Implement a new logging utility and refine Spotify client artist retrieval logic
  ([`2a20b27`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/2a20b27b9dbee31c04082298fc0dd8007ba0d2aa))

- **config**: Modularize UI components into new files
  ([`0781ca9`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/0781ca9610e8cafbd900d3867a32354244f9cd67))

- **test**: Add comprehensive test suite for Genius and Spotify API clients, including VCR cassettes
  and test utilities.
  ([`9d10fcf`](https://github.com/matiagimenez/spotify-vibe-searcher/commit/9d10fcfd28146481e12dea4fd981775fa05a2e7d))
