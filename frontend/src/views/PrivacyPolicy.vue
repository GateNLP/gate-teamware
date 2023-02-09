<template>
  <div>
    <h1>{{ productName }} Privacy Policy</h1>

    Last updated: 10th January 2023
    
    We are committed to protecting your privacy and understand that when you give us personal information you expect and trust us to take proper care with it. This policy explains what data we store about you, how we use it, and your rights to see the data we hold. If you have any queries concerning the personal data we hold or our processing of it, please contact us.

    <h3>Our contact details</h3>
    {{ contact_details }}

    <h2>The information we collect and how we use it.</h2>
    When you register an account with {{ productName }}, we collect your email address, username, first and last name and password.
    Passwords are not stored in plain text, only as hashed text strings.

    <h2>Who we share data with.</h2>
    The only service we share data with is <a href="https://www.gate.ac.uk">GATE</a>, the research team behind {{ productName }}. This does not include any personal data, only statistics on the numbers of documents and annotators.

  </div>
</template>
<script>

export default {
  name: "Privacy Policy",
  title: 'Privacy Policy',
  data: () => ({
    productName: "Teamware",
    privacyPolicySettings: version
  }),
  methods:{

  }


}
</script>
