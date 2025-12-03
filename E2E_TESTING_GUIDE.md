# E2E Testing Setup Guide

## Overview

This project uses **Cypress** for End-to-End (E2E) testing. Cypress provides an interactive testing environment for testing the complete user workflows in the Swap platform.

## Test Coverage

The E2E test suite covers the following critical user journeys:

### 1. **Authentication** (`cypress/e2e/auth.cy.ts`)

- ✅ Login page functionality
- ✅ User registration flow
- ✅ Email verification
- ✅ Error handling for invalid credentials
- ✅ Navigation between auth pages

### 2. **Listings** (`cypress/e2e/listings.cy.ts`)

- ✅ Browse all listings
- ✅ Search by keywords
- ✅ Filter by category, condition, price
- ✅ View listing details
- ✅ View seller information

### 3. **Offers** (`cypress/e2e/offers.cy.ts`)

- ✅ Create new offer
- ✅ View received/sent offers
- ✅ Filter offers by status
- ✅ Negotiate offer details
- ✅ Accept/reject offers
- ✅ Send messages during negotiation

### 4. **Chat** (`cypress/e2e/chat.cy.ts`)

- ✅ View conversations
- ✅ Send and receive messages
- ✅ Message timestamps display
- ✅ Long message handling
- ✅ Unread message indicators

### 5. **Wallet** (`cypress/e2e/wallet.cy.ts`)

- ✅ View wallet balance
- ✅ Display available and escrow balances
- ✅ Add funds (topup)
- ✅ Withdraw funds
- ✅ Transaction history
- ✅ Filter and sort transactions

## Installation

### 1. Install Cypress and Dependencies

```bash
cd /path/to/swap

npm install --save-dev cypress @cypress/webpack-dev-server @cypress/schematic

# Or with specific version
npm install --save-dev cypress@latest
```

### 2. Verify Installation

```bash
npx cypress --version
# Should output: Cypress 13.x.x or similar
```

## Running Tests

### Open Cypress Interactive Mode

```bash
# From project root
npx cypress open

# Choose E2E Testing
# Select your browser (Chrome, Firefox, Edge, Electron)
# Select a test file to run
```

### Run Tests in Headless Mode (CI/CD)

```bash
# Run all tests
npx cypress run

# Run specific test file
npx cypress run --spec "cypress/e2e/auth.cy.ts"

# Run with specific browser
npx cypress run --browser chrome

# Run with video recording
npx cypress run --record
```

### Add npm Scripts

Update `package.json` in the project root:

```json
{
  "scripts": {
    "test": "cypress run",
    "test:open": "cypress open",
    "test:auth": "cypress run --spec 'cypress/e2e/auth.cy.ts'",
    "test:listings": "cypress run --spec 'cypress/e2e/listings.cy.ts'",
    "test:offers": "cypress run --spec 'cypress/e2e/offers.cy.ts'",
    "test:chat": "cypress run --spec 'cypress/e2e/chat.cy.ts'",
    "test:wallet": "cypress run --spec 'cypress/e2e/wallet.cy.ts'",
    "test:all": "cypress run --spec 'cypress/e2e/**/*.cy.ts'"
  }
}
```

Then run:

```bash
npm run test:open
npm run test:auth
npm run test:all
```

## Test Structure

Each test file follows this structure:

```typescript
describe("Feature Name", () => {
  beforeEach(() => {
    // Setup: Navigate to page before each test
    cy.visit("/path");
  });

  describe("Sub-feature", () => {
    it("should do something", () => {
      // Arrange: Set up test data
      // Act: Perform user action
      cy.get("button").click();
      // Assert: Verify result
      cy.url().should("include", "/new-page");
    });
  });
});
```

## Key Cypress Concepts

### Selectors

```typescript
// CSS selectors
cy.get(".button-class");
cy.get("#element-id");
cy.get('input[name="email"]');

// Data-testid attributes (recommended)
cy.get('[data-testid="login-button"]');

// Contains text
cy.contains("Click me");
cy.contains("button", "Submit");
```

### Interactions

```typescript
// Typing
cy.get("input").type("user@example.com");

// Clicking
cy.get("button").click();

// Selecting dropdown
cy.get("select").select("Option 1");

// Checking checkbox
cy.get('input[type="checkbox"]').check();

// Unchecking
cy.get('input[type="checkbox"]').uncheck();
```

### Assertions

```typescript
// Visibility
cy.get("element").should("be.visible");

// Text content
cy.contains("Welcome").should("exist");

// URL
cy.url().should("include", "/dashboard");

// Value
cy.get("input").should("have.value", "test@example.com");

// Number of elements
cy.get(".item").should("have.length", 5);

// Classes
cy.get("button").should("have.class", "active");

// Disabled state
cy.get("button").should("be.disabled");
```

### Waiting

```typescript
// Wait for element
cy.get('[data-testid="loading"]').should("not.exist");

// Wait for request
cy.intercept("POST", "/api/auth/login").as("login");
cy.get("button").click();
cy.wait("@login").its("response.statusCode").should("equal", 200);

// Wait for navigation
cy.url().should("include", "/dashboard");
```

## Best Practices

### 1. Use Data-TestID Attributes

Instead of relying on implementation details, add test IDs to your components:

```jsx
// In React component
<button data-testid="submit-button">Submit</button>;

// In test
cy.get('[data-testid="submit-button"]').click();
```

### 2. Page Objects Pattern

Create reusable page objects for complex pages:

```typescript
// cypress/pages/LoginPage.ts
export class LoginPage {
  visit() {
    cy.visit("/auth/login");
  }

  fillEmail(email: string) {
    cy.get('input[name="email"]').type(email);
  }

  fillPassword(password: string) {
    cy.get('input[name="password"]').type(password);
  }

  submit() {
    cy.contains("button", "Sign In").click();
  }
}

// In test
import { LoginPage } from "../pages/LoginPage";

const loginPage = new LoginPage();
loginPage.visit();
loginPage.fillEmail("user@example.com");
loginPage.fillPassword("Password123!");
loginPage.submit();
```

### 3. Test Data Management

Use fixtures for consistent test data:

```typescript
// cypress/fixtures/user.json
{
  "email": "test@example.com",
  "password": "TestPass123!",
  "username": "testuser"
}

// In test
cy.fixture('user').then((user) => {
  cy.get('input[name="email"]').type(user.email);
});
```

### 4. API Mocking (Optional)

```typescript
cy.intercept("GET", "/api/listings", { fixture: "listings.json" }).as(
  "getListings"
);
cy.visit("/listings");
cy.wait("@getListings");
```

## Debugging Tests

### Debug Commands

```typescript
// Print element
cy.get("button").debug();

// Pause test
cy.pause();

// Get element and explore in console
cy.get("button").then(($btn) => {
  console.log($btn);
});
```

### Run in Debug Mode

```bash
npx cypress run --headed --no-exit
```

### Time Travel (in Cypress UI)

- Open Cypress UI
- Click on test step to see state at that point
- Hover over elements to highlight them

## Configuration

### Environment Variables

Create `cypress.env.json`:

```json
{
  "apiUrl": "http://localhost:8080",
  "baseUrl": "http://localhost:3000",
  "testUser": "test@example.com",
  "testPassword": "TestPass123!"
}
```

Access in tests:

```typescript
const apiUrl = Cypress.env("apiUrl");
```

### Custom Commands

Create `cypress/support/commands.ts`:

```typescript
Cypress.Commands.add("login", (email: string, password: string) => {
  cy.visit("/auth/login");
  cy.get('input[name="email"]').type(email);
  cy.get('input[name="password"]').type(password);
  cy.contains("button", "Sign In").click();
  cy.url().should("include", "/dashboard");
});

// Use in tests
cy.login("user@example.com", "Password123!");
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install dependencies
        run: npm install

      - name: Start services
        run: docker-compose up -d

      - name: Wait for services
        run: sleep 30

      - name: Run E2E tests
        run: npm run test

      - name: Upload videos
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: cypress-videos
          path: cypress/videos
```

## Troubleshooting

### Common Issues

**Issue**: Tests timeout waiting for element

```
Solution: Check if element exists, use longer timeout
cy.get('element', { timeout: 10000 })
```

**Issue**: Tests fail locally but pass in CI

```
Solution: Ensure services are running, check environment variables
```

**Issue**: Flaky tests (intermittent failures)

```
Solution: Add explicit waits, use cy.intercept for API calls
```

### Getting Help

```bash
# Open Cypress documentation
npx cypress open --help

# Run with debug output
DEBUG=* npx cypress run
```

## Next Steps

1. **Update Components**: Add `data-testid` attributes to frontend components
2. **Write More Tests**: Expand test coverage for edge cases
3. **CI/CD Setup**: Integrate tests into GitHub Actions workflow
4. **Visual Testing**: Consider adding Percy or Applitools for visual regression
5. **Performance Testing**: Add Lighthouse or WebVitals monitoring

## Resources

- [Cypress Documentation](https://docs.cypress.io/)
- [Cypress Best Practices](https://docs.cypress.io/guides/references/best-practices)
- [Testing React Components](https://docs.cypress.io/guides/component-testing/overview)
- [API Testing](https://docs.cypress.io/guides/end-to-end-testing/testing-your-app)
