// cypress/e2e/chat.cy.ts
describe("Chat Feature", () => {
  beforeEach(() => {
    cy.visit("/chat");
  });

  describe("Chat Interface", () => {
    it("should display chat page", () => {
      cy.contains("Messages").should("be.visible").or.contains("Chat");
      cy.get('[data-testid="conversations-list"]').should("be.visible");
      cy.get('[data-testid="message-input"]').should("be.visible");
    });

    it("should display conversations", () => {
      cy.get('[data-testid="conversation-item"]').should(
        "have.length.greaterThan",
        0
      );
    });

    it("should select conversation", () => {
      cy.get('[data-testid="conversation-item"]').first().click();
      cy.get('[data-testid="message-display"]').should("be.visible");
    });
  });

  describe("Messaging", () => {
    beforeEach(() => {
      cy.get('[data-testid="conversation-item"]').first().click();
    });

    it("should display messages", () => {
      cy.get('[data-testid="message"]').should("have.length.greaterThan", 0);
    });

    it("should send message", () => {
      const message = "Hello, are you interested in this item?";
      cy.get('[data-testid="message-input"]').type(message);
      cy.get('button[type="submit"]').click();
      cy.get('[data-testid="message"]').last().should("contain", message);
    });

    it("should display message timestamps", () => {
      cy.get('[data-testid="message-timestamp"]').should(
        "have.length.greaterThan",
        0
      );
    });

    it("should handle long messages", () => {
      const longMessage =
        "This is a very long message that should be properly wrapped and displayed on the screen. " +
        "It contains multiple sentences and should maintain readability.";
      cy.get('[data-testid="message-input"]').type(longMessage);
      cy.get('button[type="submit"]').click();
      cy.get('[data-testid="message"]')
        .last()
        .should("contain", "very long message");
    });
  });

  describe("Conversation Management", () => {
    it("should mark conversation as read", () => {
      cy.get('[data-testid="conversation-item"][data-unread="true"]')
        .first()
        .click();
      cy.get('[data-testid="conversation-item"][data-unread="true"]').should(
        "not.exist"
      );
    });

    it("should show unread count", () => {
      cy.get('[data-testid="unread-badge"]')
        .should("be.visible")
        .or.contains(/^\d+$/);
    });
  });
});
