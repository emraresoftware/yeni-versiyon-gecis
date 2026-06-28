# Task 009 Mobile Report — Registered Accounts Login & Demo Agent Integration

## Objective
Implement registered accounts authentication and live Demo Assistant features in the Android Kotlin superapp, pointing to `https://aiasistan.emarecloud.tr/demo-agent` and ensuring a seamless, automated login experience using Web Storage injection.

## Scope
- Modify the Android Kotlin project at `/Users/emre/Emare superapp`.
- Update network client to use `aiasistan.emarecloud.tr` instead of `app.emarecloud.tr`.
- Implement dynamic session storage and credentials saving in SharedPreferences.
- Redesign the Login screen to accept registered Email and Password.
- Inject the user session automatically into the WebView local storage to bypass redundant web login.
- Ensure compat methods remain intact to avoid other activities' compile errors.

## Files Created
None (refactored and added code within existing classes/layouts).

## Files Modified
- [ApiClient.kt](file:///Users/emre/Emare%20superapp/app/src/main/java/com/emaresuperapp/crm/api/ApiClient.kt)
- [ApiService.kt](file:///Users/emre/Emare%20superapp/app/src/main/java/com/emaresuperapp/crm/api/ApiService.kt)
- [SessionManager.kt](file:///Users/emre/Emare%20superapp/app/src/main/java/com/emaresuperapp/crm/util/SessionManager.kt)
- [SplashActivity.kt](file:///Users/emre/Emare%20superapp/app/src/main/java/com/emaresuperapp/crm/SplashActivity.kt)
- [LoginActivity.kt](file:///Users/emre/Emare%20superapp/app/src/main/java/com/emaresuperapp/crm/LoginActivity.kt)
- [activity_login.xml](file:///Users/emre/Emare%20superapp/app/src/main/res/layout/activity_login.xml)
- [DashboardFragment.kt](file:///Users/emre/Emare%20superapp/app/src/main/java/com/emaresuperapp/crm/ui/dashboard/DashboardFragment.kt)
- [ProfilFragment.kt](file:///Users/emre/Emare%20superapp/app/src/main/java/com/emaresuperapp/crm/ui/profil/ProfilFragment.kt)

## Architecture Decisions
- **Hybrid WebView Synchronization:** Instead of recreating the 18 demo scenarios and their dynamic parameters in Android Kotlin native UI (which would require a new APK compile and reinstall for every small change), we utilized the live webapp route `/demo-agent`.
- **Zustand LocalStorage Injection:** On WebView load, the native app dynamically serializes the logged-in user's credentials and tokens from SharedPreferences and injects them directly into the WebView's `localStorage` (key: `auth-storage`). This ensures the user is logged in instantly without seeing any login prompts.
- **Compatibility Methods:** Maintained old methods (`saveCredentials`, etc.) with safe fallbacks in `SessionManager` so that other modules (like `RegisterActivity`) compile successfully.

## Dependencies Added
None.

## Build Result
- Tested using `./gradlew assembleDebug` in the project directory.
- Compile Result: **SUCCESSFUL** (compiled cleanly in 5 seconds).

## Test Result
- Verified build and class mappings. All Kotlin compiler warnings resolved or handled.

## Performance Notes
- Token injection is performed both at `onPageStarted` and `onPageFinished` to guarantee it is written before the JS application attempts hydration.
- The `ProfilFragment` pulls info instantly from SharedPreferences, avoiding unnecessary blocking network requests.

## Security Notes
- Secure HTTPS is enforced on `aiasistan.emarecloud.tr` connections.
- JWT access tokens and refresh tokens are securely stored in private SharedPreferences.
- Header interceptor automatically adds `Authorization: Bearer <token>` to retrofitted calls if the token is present.

## Technical Debt
- Biometric login (FaceID / Fingerprint) and dynamic session refresh logic could be added in a future sprint.

## Risks
- WebView DOM storage changes: If the frontend changes the storage key name from `auth-storage` in `useAuthStore`, the injection will need to be updated.

## Known Limitations
- The app requires an active internet connection to load the hybrid WebView components.

## Breaking Changes
- The app no longer accepts or validates the `token` invite-codes for the main dashboard login; it now requires valid email/password credentials of registered accounts.

## Next Recommended Task
- Set up push notifications (FCM) linked to the user's tenant scope.
