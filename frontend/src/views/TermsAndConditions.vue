<template>
  <div class="container" v-if="!privacyPolicyDetails.CUSTOM_TC_DOCUMENT">
    
    <h1>Terms & Conditions</h1>
    <p>
    Last updated: {{ lastUpdated }}
    <br><br>
    These terms and conditions (the “Terms and Conditions”) govern the use of {{ productName }}. {{ productName }} is owned and operated by the Host on behalf of the Administrator. {{ productName }} is a service.
    <br>
    By using {{ productName }}, you indicate that you have read and understand these Terms and Conditions and agree to abide by them at all times.
    </p>
    <h2>Definitions</h2>
    <p>
    <ul>
    <li><strong>Host</strong>: The individual or organisation responsible for maintaining the deployment {{ productName }} either on their own hardware or that of a third-party provider. The host may also be responsible for installing {{ productName }}, updating, running and ceasing the running of {{ productName }} at {{ privacyPolicyDetails.URL }}.</li>
    <li><strong>Administrator</strong>: The individual(s) or team of individuals responsible for the creation and management of user accounts and projects across {{ privacyPolicyDetails.URL }}.</li>
    </ul>
    </p>
    <p>
    <h2>Intellectual Property</h2>
    All content published and made available using {{ productName }} is the property of the Host, Administrator and {{ productName }}’s creators. 
    This includes but is not limited to images, text logos, documents, downloadable files and anything that contributes to the composition of our Site.
    </p>
    <h2>Acceptable Use</h2>
    <p>
    As a user of {{ productName }}, you agree to use {{ productName }} legally, not to use {{ productName }} for illegal purposes, and not to:
    <br>
    <ul>
    <li>Harass and mistreat other users of {{ productName }};</li>
    <li>Violate the rights of other users of {{ productName }};</li>
    <li>Violate the intellectual property rights of the {{ productName }} owners or any third party to {{ productName }};</li>
    <li>Hack into the account of another user of {{ productName }};</li>
    <li>Act in any way that could be considered fraudulent; or</li>
    <li>Post any material that may be deemed inappropriate or offensive.</li>
    </ul>
    If it is believed that you are using {{ productName }} illegally or in a manner that violates these Terms and Conditions, the Host reserves the right to limit, suspend or terminate your access to {{ productName }}. The Host also reserves the right to take any legal steps necessary to prevent you from accessing {{ productName }}.
    </p>
    <h2>User Contributions</h2>
    <p>
    Users may post the following information on {{ productName }}:
    <ul>
    <li>Documents; and</li>
    <li>Annotations.</li>
    </ul>
    By adding information to {{ productName }}, you agree to not act illegally or violate these Terms and Conditions.
    </p>
    <h2>Accounts</h2>
    <p>
    When you create a {{ productName }} account, you agree to the following:
    <br>
    You are solely responsible for your account and the security and privacy of your account, including passwords or sensitive information attached to that account; and
    All personal information you provide to use through your account is up to date, accurate, and truthful and that you will update your personal information if it changes.
    <br>
    The Host reserves the right to suspend or terminate your account if you are using {{ productName }} illegally or if you violate these Terms and Conditions.
    </p>
    <p>
    <h2>Limitation of Liability</h2>
    The Host and our directors, officers, agents, employees, subsidiaries, and affiliates will not be liable for any actions, claims, losses, damages, liabilities and expenses including legal fees from your use of {{ productName }}.
    </p>
    <h2>Indemnity</h2>
    <p>
    Except where prohibited by law, by using {{ productName }} you indemnify and hold harmless the Host and our directors, officers, agents, employees, subsidiaries, and affiliates from any actions, claims, losses, damages, liabilities and expenses including legal fees arising out of your use of {{ productName }} or your violation of these Terms and Conditions.
    </p>
    <h2>Applicable Law</h2>
    <p>
    These Terms and Conditions are governed by the laws of the Country of England.
    </p>
    <h2>Severability</h2>
    <p>
    If at any time any of the provisions set forth in these Terms and Conditions are found to be inconsistent of invalid under applicable laws, those provisions will be deemed void and will be removed from these Terms and Conditions. All other provisions will not be affected by the removal and the rest of these Terms and Conditions will still be considered valid.
    </p>
    <h2>Changes</h2>
    <p>
    These Terms and Conditions may be amended from time to time in order to maintain compliance with the law and to reflect any changes to the way we operate {{ productName }} and the way we expect users to behave using {{ productName }}. We will notify users by email of changes to these Terms and Conditions or post a notice on the site.
    </p>
    <h2>Contact Details</h2>
    <p>
    Please contact us if you have any questions or concerns. Our contact details are as follows:
    <br><br>
    <div style="width: 100%; overflow: hidden;">
      <div style="width: 600px; float: left;">
        <h3>Host</h3>
          <p>Name: {{ privacyPolicyDetails.HOST_NAME }}</p>
          <p>Address: {{ privacyPolicyDetails.HOST_ADDRESS }}</p>
          <p>Contact: <span v-html="privacyPolicyDetails.HOST_CONTACT"></span></p>
        </div>
        <div style="margin-left: 620px;">
          <h3>Administrator</h3>
          <p>Name: {{ privacyPolicyDetails.ADMIN_NAME }}</p>
          <p>Address: {{ privacyPolicyDetails.ADMIN_ADDRESS }}</p>
          <p>Contact: <span v-html="privacyPolicyDetails.ADMIN_CONTACT"></span></p>
      </div>
    </div>
    <br><br>
    </p>

  </div>

  <div class="container" v-else>
    <MarkdownRenderer :content="privacyPolicyDetails.CUSTOM_TC_DOCUMENT"></MarkdownRenderer>
  </div>
</template>
<script>

import {mapActions} from 'vuex'
import MarkdownRenderer from "@/components/MarkdownRenderer";

export default {
  name: "Terms & Conditions",
  title: 'Terms & Conditions',
  components: {MarkdownRenderer},
  data: () => ({
    lastUpdated: "9th March 2023",
    productName: "Teamware",
    privacyPolicyDetails: {}
  }),
  methods:{
    ...mapActions(["getPrivacyPolicyDetails"]),
    async fetchPrivacyPolicyDetails(){
      this.privacyPolicyDetails = await this.getPrivacyPolicyDetails();
    }
  },
  mounted() {
    this.fetchPrivacyPolicyDetails();
  }


}
</script>
