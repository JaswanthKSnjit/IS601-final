# Test Coverage Improvement Summary

- Passes all 108 tests in pytest - [here](Screenshots/pytest.png) 
- Improved the overall test coverage to 91% - [here](Screenshots/tests.png)

This section documents the 10 issues resolved through dedicated test cases to ensure high reliability and coverage of critical user features in the project.

Each test was linked to a GitHub Issue and resolved via a corresponding Pull Request.

| #  | Test Title                           | Description of Fix                                                   | Issue                                                                 | Pull Request                                                             |
|----|--------------------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------|
| 1 | **Test: weak password rejection**    | Tested password policy enforcement for weak inputs.                   | [#17](https://github.com/JaswanthKSnjit/IS601-final/issues/17)         | [PR #18](https://github.com/JaswanthKSnjit/IS601-final/pull/18)         |
| 2  | **Test: Duplicate Email Registration** | Checked duplicate email registration is blocked.                     | [#19](https://github.com/JaswanthKSnjit/IS601-final/issues/19)         | [PR #20](https://github.com/JaswanthKSnjit/IS601-final/pull/20)         |
| 3  | **Test: Login Fail**                 | Verified system handles invalid login attempts appropriately.         | [#21](https://github.com/JaswanthKSnjit/IS601-final/issues/21)         | [PR #22](https://github.com/JaswanthKSnjit/IS601-final/pull/22)         |
| 4  | **Test: Auto generated names missing** | Tested fallback nickname is generated if none provided.              | [#23](https://github.com/JaswanthKSnjit/IS601-final/issues/23)         | [PR #24](https://github.com/JaswanthKSnjit/IS601-final/pull/24)         |
| 5  | **Test: No self assign role**        | Checked user cannot assign admin/manager roles during registration.   | [#25](https://github.com/JaswanthKSnjit/IS601-final/issues/25)         | [PR #26](https://github.com/JaswanthKSnjit/IS601-final/pull/26)         |
| 6  | **Test: Restrict Access**            | Confirmed regular users can't access admin-only routes.               | [#27](https://github.com/JaswanthKSnjit/IS601-final/issues/27)         | [PR #28](https://github.com/JaswanthKSnjit/IS601-final/pull/28)         |
| 7  | **Test: Lock account after login fail** | Tested account lockout after multiple failed attempts.               | [#29](https://github.com/JaswanthKSnjit/IS601-final/issues/29)         | [PR #30](https://github.com/JaswanthKSnjit/IS601-final/pull/30)         |
| 8  | **Test: Reject Invalid Email Login** | Validated login fails with invalid email format.                      | [#31](https://github.com/JaswanthKSnjit/IS601-final/issues/31)         | [PR #32](https://github.com/JaswanthKSnjit/IS601-final/pull/32)         |
| 9  | **Test: Block duplicate email**      | Ensured users cannot update email to one already registered.          | [#33](https://github.com/JaswanthKSnjit/IS601-final/issues/33)         | [PR #34](https://github.com/JaswanthKSnjit/IS601-final/pull/34)         |
| 10  | **Test: Reset Password Length**      | Enforced password strength validation during password reset.          | [#35](https://github.com/JaswanthKSnjit/IS601-final/issues/35)         | [PR #36](https://github.com/JaswanthKSnjit/IS601-final/pull/36)         |
