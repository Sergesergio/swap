// cypress/e2e/offers.cy.ts
describe("Offers Feature", () => {
  beforeEach(() => {
    cy.visit("/offers");
  });

  describe("View Offers", () => {
    it("should display offers page", () => {
      cy.contains("Offers").should("be.visible");
      cy.get('[data-testid="offer-card"]').should("have.length.greaterThan", 0);
    });

    it("should filter by status", () => {
      cy.get('select[name="status"]').select("Pending");
      cy.get('[data-testid="offer-card"]').should("exist");
    });

    it("should navigate to offer detail", () => {
      cy.get('[data-testid="offer-card"]').first().click();
      cy.url().should("include", "/offers/");
    });
  });

  describe("Make Offer", () => {
    beforeEach(() => {
      cy.visit("/listings/123");
      cy.contains("button", "Make Offer").click();
    });

    it("should display make offer form", () => {
      cy.get('input[name="items_offered"]').should("be.visible");
      cy.get('input[name="money_add_on"]').should("be.visible");
      cy.contains("button", "Submit Offer").should("be.visible");
    });

    it("should submit offer", () => {
      cy.get('input[name="money_add_on"]').type("50.00");
      cy.contains("button", "Submit Offer").click();
      cy.contains("Offer submitted successfully")
        .should("be.visible")
        .or.contains("success");
    });
  });

  describe("Offer Negotiation", () => {
    beforeEach(() => {
      cy.visit("/offers/456");
    });

    it("should display offer details", () => {
      cy.contains("Offer Details").should("be.visible").or.contains("Status");
      cy.contains("Your Items").should("be.visible");
      cy.contains("Their Items").should("be.visible");
    });

    it("should display negotiation chat", () => {
      cy.get('[data-testid="chat-messages"]').should("be.visible");
      cy.get('input[placeholder*="message"]').should("be.visible");
    });

    it("should send message in negotiation", () => {
      cy.get('input[placeholder*="message"]').type(
        "Are you willing to add more items?"
      );
      cy.get('button[type="submit"]').click();
      cy.get('[data-testid="chat-messages"]').should(
        "contain",
        "Are you willing to add more items?"
      );
    });

    it("should accept offer", () => {
      cy.contains("button", "Accept Offer").click();
      cy.contains("Offer accepted").should("be.visible").or.contains("success");
    });

    it("should reject offer", () => {
      cy.contains("button", "Reject Offer").click();
      cy.contains("Confirm rejection").should("be.visible");
      cy.contains("Yes, reject").click();
    });
  });
});
