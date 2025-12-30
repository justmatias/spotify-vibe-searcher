# CHANGELOG


## v0.3.0 (2025-12-29)

### Bug Fixes

- **config**: Declare sub-containers using `providers.Container` for lazy loading.
  ([`a8b9cea`](https://github.com/matiagimenez/spotify-rag/commit/a8b9ceaa9df72902b47dae733981c4120c52119c))

- **test**: Implement tests for the LibrarySyncService and dependency injection container
  ([`1bf5272`](https://github.com/matiagimenez/spotify-rag/commit/1bf527294aede4f9662f22370490e61d30424ac8))

### Chores

- **config**: Remove docstring from `injections` container.
  ([`46bec22`](https://github.com/matiagimenez/spotify-rag/commit/46bec22eb5ef02c0d556cdee5787036f84c7972b))

- **config**: Update requirements.txt
  ([`baa41a2`](https://github.com/matiagimenez/spotify-rag/commit/baa41a2ea258fc8f4e1bfc6f31f20a71ab1c0cc6))

### Features

- **config**: Implement library synchronization with track enrichment and dependency injection for
  services and infrastructure
  ([`7172b12`](https://github.com/matiagimenez/spotify-rag/commit/7172b129b00994eacf1eb036db5261828be75e65))

### Refactoring

- **config**: Update DI container instantiation to directly create sub-containers and pass
  dependencies.
  ([`aaffc00`](https://github.com/matiagimenez/spotify-rag/commit/aaffc001b6e0162fc6a1e8f4448ecf6a3da69eb1))


## v0.2.0 (2025-12-29)

### Chores

- **config**: Update pyproject.toml
  ([`50f1d6c`](https://github.com/matiagimenez/spotify-rag/commit/50f1d6c4fc41c9995e5fb890dbd701cb8f69e37f))

- **deps**: Bump actions/checkout from 4 to 6
  ([`1a9295d`](https://github.com/matiagimenez/spotify-rag/commit/1a9295d8778a2690d780bb7884aa4d7e10956392))

Bumps [actions/checkout](https://github.com/actions/checkout) from 4 to 6. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/actions/checkout/compare/v4...v6)

--- updated-dependencies: - dependency-name: actions/checkout dependency-version: '6'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump actions/setup-python from 5 to 6
  ([`676e247`](https://github.com/matiagimenez/spotify-rag/commit/676e2472835f7e287c8e3432ca0c13a9c69189cc))

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 5 to 6. - [Release
  notes](https://github.com/actions/setup-python/releases) -
  [Commits](https://github.com/actions/setup-python/compare/v5...v6)

--- updated-dependencies: - dependency-name: actions/setup-python dependency-version: '6'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump peter-evans/create-pull-request from 7 to 8
  ([`720c37c`](https://github.com/matiagimenez/spotify-rag/commit/720c37c9ac569e64cb6552296ccad5234ea7791a))

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
  ([`d943b71`](https://github.com/matiagimenez/spotify-rag/commit/d943b71ac24d460cff0b3fbb391c617f7b526cbe))


## v0.1.1 (2025-12-29)

### Bug Fixes

- **test**: Initialize app settings with test credentials
  ([`7f26d8c`](https://github.com/matiagimenez/spotify-rag/commit/7f26d8cecf7b6baf2fa99ef818958e0ce99fb8b1))

### Chores

- **config**: Adjust type ignore comment in Spotify client
  ([`2414b94`](https://github.com/matiagimenez/spotify-rag/commit/2414b9468cbf3d81cced656ce962f775c1ef67f9))


## v0.1.0 (2025-12-29)

### Bug Fixes

- **config**: Fix spotify client instantiation
  ([`01eca70`](https://github.com/matiagimenez/spotify-rag/commit/01eca703a624d0d8f510055811c2a314f16140e9))

### Chores

- **config**: Add GitHub Actions for CI, Dependabot, pre-commit autoupdate
  ([`d367a94`](https://github.com/matiagimenez/spotify-rag/commit/d367a943513af9fea7e31c2ff7c3d692c73e45dd))

- **config**: Add pre-commit configuration.
  ([`f2719cb`](https://github.com/matiagimenez/spotify-rag/commit/f2719cb23aabdddfce68860da4fad320b6ec4cfd))

- **config**: Add project versioning
  ([`15052fe`](https://github.com/matiagimenez/spotify-rag/commit/15052fee5329f2183dd8e42feda5ff32361bafd8))

- **config**: Add security pre-commit hooks
  ([`9d3111d`](https://github.com/matiagimenez/spotify-rag/commit/9d3111d1210af48ee5555cb8318ad0757aee20af))

- **config**: Dynamically fetch package version
  ([`a3e1569`](https://github.com/matiagimenez/spotify-rag/commit/a3e1569ebf1a3e0d6a0f2e91bf90d9ba51890209))

- **config**: Fix lint issues
  ([`6053279`](https://github.com/matiagimenez/spotify-rag/commit/6053279998166bc12318b601b28faa71b39a538c))

- **docs**: Add README.md
  ([`ffca9d2`](https://github.com/matiagimenez/spotify-rag/commit/ffca9d2e3a6d6d4c8b4bf3084f9b3de749b9761a))

- **docs**: Update .env.sample
  ([`01fb758`](https://github.com/matiagimenez/spotify-rag/commit/01fb7589c59ae8d639886f957a203894caf3f8ee))

- **docs**: Update implementation plan
  ([`af09cf3`](https://github.com/matiagimenez/spotify-rag/commit/af09cf310f10bf22f7ebd414435609dd081ce415))

### Features

- **config**: Add Genius API integration, new Spotify domain models, and refactor settings to use
  uppercase naming conventions.
  ([`ec2df90`](https://github.com/matiagimenez/spotify-rag/commit/ec2df90e4905bb420ba4fd7d7d720ad2a6a33f0c))

- **config**: Add Spotify authentication, API client, and user domain model, and refactor UI to use
  new infrastructure
  ([`7a33c38`](https://github.com/matiagimenez/spotify-rag/commit/7a33c385d3f30f25554a4faaec71fb1021566da9))

- **config**: Establish initial project structure, core modules, UI, and dependency management
  ([`2ce9a8e`](https://github.com/matiagimenez/spotify-rag/commit/2ce9a8e126836ea4a1394db6fa21158e68fd010c))

- **config**: Implement a new logging utility and refine Spotify client artist retrieval logic
  ([`2a20b27`](https://github.com/matiagimenez/spotify-rag/commit/2a20b27b9dbee31c04082298fc0dd8007ba0d2aa))

- **config**: Modularize UI components into new files
  ([`0781ca9`](https://github.com/matiagimenez/spotify-rag/commit/0781ca9610e8cafbd900d3867a32354244f9cd67))

- **test**: Add comprehensive test suite for Genius and Spotify API clients, including VCR cassettes
  and test utilities.
  ([`9d10fcf`](https://github.com/matiagimenez/spotify-rag/commit/9d10fcfd28146481e12dea4fd981775fa05a2e7d))
