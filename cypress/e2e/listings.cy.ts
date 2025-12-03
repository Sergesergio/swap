// cypress/e2e/listings.cy.ts
describe("Listings Feature", () => {
  beforeEach(() => {
    // Assuming user is logged in via API or fixtures
    cy.visit("/listings");
  });

  describe("Browse Listings", () => {
    it("should display listings page", () => {
      cy.contains("h1", "Browse Listings")
        .should("be.visible")
        .or.contains("Listings");
      cy.get('[data-testid="listing-card"]').should(
        "have.length.greaterThan",
        0
      );
    });

    it("should display search input", () => {
      cy.get('input[placeholder*="Search"]').should("be.visible");
    });

    it("should search listings", () => {
      cy.get('input[placeholder*="Search"]').type("laptop");
      cy.get("button").contains("Search").click();
      // Verify filtered results
      cy.get('[data-testid="listing-card"]').should(
        "have.length.greaterThan",
        0
      );
    });

    it("should filter by category", () => {
      cy.get('select[name="category"]').select("Electronics");
      cy.get('[data-testid="listing-card"]').should("exist");
    });

    it("should filter by price range", () => {
      cy.get('input[name="minPrice"]').type("100");
      cy.get('input[name="maxPrice"]').type("1000");
      cy.contains("button", "Apply Filters").click();
    });

    it("should navigate to listing detail", () => {
      cy.get('[data-testid="listing-card"]').first().click();
      cy.url().should("include", "/listings/");
      cy.contains("Item Details")
        .should("be.visible")
        .or.contains("Description");
    });
  });

  describe("Listing Detail View", () => {
    beforeEach(() => {
      cy.visit("/listings/123"); // Assuming listing ID 123 exists
    });

    it("should display listing details", () => {
      cy.contains("Title")
        .should("exist")
        .or.contains(/^[A-Z]/);
      cy.contains("Description").should("exist").or.contains("Condition");
      cy.contains("Price").should("exist").or.contains("$");
    });

    it("should display images", () => {
      cy.get('img[alt*="item"]').should("have.length.greaterThan", 0);
    });

    it("should display seller info", () => {
      cy.contains("Seller").should("exist").or.contains("Rating");
    });

    it("should have make offer button", () => {
      cy.contains("button", "Make Offer")
        .should("be.visible")
        .or.contains("Swap");
    });
  });
});
