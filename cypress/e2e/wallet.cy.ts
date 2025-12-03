// cypress/e2e/wallet.cy.ts
describe("Wallet Feature", () => {
  beforeEach(() => {
    cy.visit("/wallet");
  });

  describe("Wallet Display", () => {
    it("should display wallet page", () => {
      cy.contains("Wallet").should("be.visible").or.contains("Balance");
      cy.get('[data-testid="balance-display"]').should("be.visible");
    });

    it("should display available balance", () => {
      cy.get('[data-testid="available-balance"]')
        .should("be.visible")
        .and("contain", "$");
    });

    it("should display escrow balance", () => {
      cy.get('[data-testid="escrow-balance"]')
        .should("be.visible")
        .and("contain", "$");
    });

    it("should display transaction history", () => {
      cy.get('[data-testid="transaction-history"]').should("be.visible");
      cy.get('[data-testid="transaction-item"]').should(
        "have.length.greaterThan",
        0
      );
    });
  });

  describe("Add Funds (Topup)", () => {
    beforeEach(() => {
      cy.contains("button", "Add Funds").click();
    });

    it("should display topup form", () => {
      cy.get('input[name="amount"]').should("be.visible");
      cy.contains("button", "Continue to Payment")
        .should("be.visible")
        .or.contains("Proceed");
    });

    it("should validate amount", () => {
      cy.get('input[name="amount"]').type("0");
      cy.contains("button", "Continue to Payment").click();
      cy.contains("Invalid amount").should("be.visible").or.contains("minimum");
    });

    it("should process topup", () => {
      cy.get('input[name="amount"]').type("100.00");
      cy.contains("button", "Continue to Payment").click();
      // Would redirect to payment processor or show payment modal
      cy.url().should("not.include", "/wallet").or.contains("payment");
    });
  });

  describe("Withdraw Funds", () => {
    beforeEach(() => {
      cy.contains("button", "Withdraw").click();
    });

    it("should display withdraw form", () => {
      cy.get('input[name="amount"]').should("be.visible");
      cy.get('select[name="bankAccount"]').should("be.visible");
      cy.contains("button", "Request Withdrawal")
        .should("be.visible")
        .or.contains("Withdraw");
    });

    it("should validate withdrawal amount", () => {
      cy.get('input[name="amount"]').type("0");
      cy.contains("button", "Request Withdrawal").click();
      cy.contains("Invalid amount").should("be.visible").or.contains("minimum");
    });

    it("should process withdrawal request", () => {
      cy.get('input[name="amount"]').type("50.00");
      cy.get('select[name="bankAccount"]').select("Primary Account");
      cy.contains("button", "Request Withdrawal").click();
      cy.contains("Withdrawal requested")
        .should("be.visible")
        .or.contains("success");
    });
  });

  describe("Transaction History", () => {
    it("should display transaction details", () => {
      cy.get('[data-testid="transaction-item"]').first().click();
      cy.get('[data-testid="transaction-detail"]').should("be.visible");
      cy.contains("Transaction ID").should("be.visible");
      cy.contains("Amount").should("be.visible");
      cy.contains("Status").should("be.visible");
    });

    it("should filter transactions", () => {
      cy.get('select[name="filterType"]').select("Deposits");
      cy.get('[data-testid="transaction-item"]').each(($el) => {
        cy.wrap($el).should("contain", "Deposit").or.contains("payment.held");
      });
    });

    it("should sort transactions", () => {
      cy.contains("button", "Sort").click();
      cy.get('select[name="sortBy"]').select("Date - Newest First");
      // Verify first transaction is most recent
    });
  });
});
