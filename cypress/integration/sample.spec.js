describe('My First Test', () => {

    beforeEach(()=>{
        // cy.exec('npm run serve')
    })

  it('Does not do much!', () => {
      cy.visit("")
      cy.contains('Gate Annotation Tool')
      cy.contains('About').click()
      cy.contains('This is an about page')
      expect(true).to.equal(false)
  })
})
