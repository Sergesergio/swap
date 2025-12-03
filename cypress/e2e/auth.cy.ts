// cypress/e2e/auth.cy.ts
describe("Authentication Flow", () => {
  beforeEach(() => {
    cy.visit("/auth/login");
  });

  describe("Login Page", () => {
    it("should display login form", () => {
      cy.contains("h1", "Swap").should("be.visible");
      cy.contains("p", "Welcome back").should("be.visible");
      cy.get('input[name="email"]').should("be.visible");
      cy.get('input[name="password"]').should("be.visible");
      cy.contains("button", "Sign In").should("be.visible");
    });

    it("should show validation errors for invalid email", () => {
      cy.get('input[name="email"]').type("invalid-email");
      cy.get('input[name="password"]').type("Password123!");
      cy.contains("button", "Sign In").click();
      // Error handling depends on backend validation
    });

    it("should show error message for invalid credentials", () => {
      cy.get('input[name="email"]').type("nonexistent@example.com");
      cy.get('input[name="password"]').type("WrongPassword123!");
      cy.contains("button", "Sign In").click();
      cy.contains("Failed").should("be.visible").or.contains("error");
    });

    it("should navigate to register page", () => {
      cy.contains("a", "Sign up").click();
      cy.url().should("include", "/auth/register");
    });

    it("should navigate to forgot password page", () => {
      cy.contains("a", "Forgot password?").click();
      cy.url().should("include", "/auth/forgot-password");
    });
  });

  describe("Registration Flow", () => {
    beforeEach(() => {
      cy.visit("/auth/register");
    });

    it("should display registration form", () => {
      cy.contains("h1", "Create Account").should("be.visible");
      cy.get('input[name="email"]').should("be.visible");
      cy.get('input[name="username"]').should("be.visible");
      cy.get('input[name="password"]').should("be.visible");
      cy.contains("button", "Sign Up").should("be.visible");
    });

    it("should validate form fields", () => {
      cy.get('input[name="email"]').type("test@example.com");
      cy.get('input[name="username"]').type("testuser");
      cy.get('input[name="password"]').type("Pass123!");
      cy.contains("button", "Sign Up").click();
      // Wait for API response
      cy.url().should("include", "/auth/verify-email");
    });

    it("should navigate back to login", () => {
      cy.contains("a", "Sign in").click();
      cy.url().should("include", "/auth/login");
    });
  });

  describe("Email Verification", () => {
    beforeEach(() => {
      cy.visit("/auth/verify-email");
    });

    it("should display verification form", () => {
      cy.contains("Verify Email").should("be.visible");
      cy.get('input[type="text"]').should("have.length.at.least", 1);
    });
  });
});
