<template>
  <div class="container" v-if="!privacyPolicyDetails.CUSTOM_PP_DOCUMENT">
    <h1>{{ productName }} Privacy Policy</h1>

    <p>Last updated: {{ lastUpdated }}</p>
    
    <p>
    <h2>Definitions of Roles and Terminology</h2>

    For the purposes of this privacy policy the following roles are defined. Note that in some cases, the Host and Administrator (and/or the Project Manager) may constitute the same individual or organisation.

    <ul>
    <li><strong>{{ productName }}</strong>: The open source software that implements a {{ productName }} server, developed by GATE.</li>
    <li><strong>{{ productName }} Instance</strong>: A single running implementation of {{ productName }} running at a unique URL. User accounts and data on a single instance are not shared with or transferable to other instances and administrators/project managers do not necessarily have the same privileges on other instances.</li>
    <li><strong>Host</strong>: The individual or organisation responsible for maintaining the deployment of this {{ productName }} instance either on their own hardware or that of a third-party provider. The host may also be responsible for installing {{ productName }}, updating, running and ceasing the running of the {{ productName }} instance.</li>
    <li><strong>Administrator</strong>: The individual(s) or team of individuals responsible for the creation and management of user accounts and projects across the entire {{ productName }} instance. Administrators have {{ productName }} user accounts with elevated privileges.</li>
    <li><strong>Project Manager</strong>: Individuals with user accounts with elevated privileges on the {{ productName }} instance to create and delete projects.</li>
    <li><strong>Annotator</strong>: The default user account type for individuals registering with a {{ productName }} instance, used primarily for users who are assigned annotation tasks. Annotators do not have access to manage projects or users. Note that the act of annotation can also be performed by users who are project managers or administrators.</li>
    </ul>
    </p>
    <p>
    <h2>Contact Details</h2>
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
    </p>
    <p>
      <h2>The type of personal information we collect</h2>
      We collect the following information:
      <ul>
      <li><strong>User Credentials</strong>: used for administrating user accounts: Email address, username, password. Passwords are not stored or accessible as plain text.</li>
      <li><strong>Document and Annotations</strong>: Documents are the text files uploaded by project managers and annotations are the labels given to them during the annotation process by annotators. Project managers are responsible for both of these types of data and administrating what is stored. Since annotations may contain free text input for annotators to fill in, it is the responsibility of project managers to warn annotators against entering any personal information into fields like this. Project managers are also responsible for meeting the requirements of the rights of users, explained below in “Your data protection rights”.</li>
      </ul>
    </p>

    <p>
      <h2>How and why {{ productName }} collects personal information</h2>
      Under the UK General Data Protection Regulation (UK GDPR), the lawful bases we rely on for processing this information are:
    </p>

    <p>
      <h3>To carry out our contract with you</h3>
      When you register for a {{ productName }} account, {{ productName }} collects your username, email address and password which are used to: 
      allow you to log in and use {{ productName }} securely; verify your identity before using the service; contact you if required regarding 
      your data, account or updates to the terms of service.
      
      When project managers and/or administrators upload documents for annotation and annotations are made, 
      data is stored for the purposes of managing annotation tasks and providing {{ productName }}’s functionality.
    </p>

    <p>
      <h3>When we believe it is in our legitimate interests</h3>
      When you use {{ productName }} the host stores your IP address in the form of request logs. Logs are not shared.
    
      When {{ productName }} projects are either completed or deleted, aggregated, anonymous data including the number of documents, 
      number of annotators, number of annotations are sent to the developers of {{ productName }}, GATE. {{ productName }} is provided as free, 
      open source software and collecting usage statistics allows GATE to demonstrate its usage to funders, 
      allowing us to support its development and maintenance.
    </p>

    <p>
      <h2>How we store personal information</h2>

      Your information is securely stored.

      Data is kept within a {{ productName }} instance as long as the instance is running; or until it is deleted. 
      Once an instance is no longer running, data will be kept for a duration according to the agreement between the host and administrator.
    </p>

    <p>
      <h2>Your data protection rights</h2>

      Under data protection law, you have rights including:<br>
      
      <strong>Your right of access</strong> - You have the right to ask the host or administrator(s) for copies of your personal information.<br>

      <strong>Your right to rectification</strong> - You have the right to ask the host or administrator(s) to rectify personal information you think is inaccurate. 
      You also have the right to ask the host or administrator(s) to complete information you think is incomplete.<br>

      <strong>Your right to erasure</strong> - You have the right to the host or administrator(s) to erase your personal information in certain circumstances. 
      Please use the facilities within {{ productName }} to delete your account if required, at which point any annotations or documents will remain, but your account will be anonymised.<br>

      <strong>Your right to restriction of processing</strong> - You have the right to ask us to restrict the processing of your personal information in certain circumstances.<br>

      <strong>Your right to object to processing</strong> - You have the right to object to the processing of your personal information in certain circumstances.<br>

      <strong>Your right to data portability</strong> - You have the right to ask that we transfer the personal information you gave us to another organisation, or to you, in certain circumstances.<br>
      <br>
      You are not required to pay any charge for exercising your rights. If you make a request, we have one month to respond to you.<br>
      
      Please contact the host and/or administrators at the contact details above if you wish to make a request.<br>

    </p>

    <p>
      <h2>How to complain</h2>
      If you have any concerns about the use of your personal information in {{ productName }}, 
      you can make a complaint to the host and or administrator at the contact details above.
      You can also complain to the Information Commissioner’s Office (ICO) if you are unhappy with how your data is used.
      <br>
      The ICO’s address:<br>
      Information Commissioner’s Office<br>
      Wycliffe House<br>
      Water Lane<br>
      Wilmslow<br>
      Cheshire<br>
      SK9 5AF<br>
      United Kingdom<br>
      <br>
      Helpline number: 0303 123 1113<br>
      ICO website: <a href="https://www.ico.org.uk">https://www.ico.org.uk</a>
      <br><br><br>
    </p>

  </div>

  <div class="container" v-else>
    <span v-html="privacyPolicyDetails.CUSTOM_PP_DOCUMENT"></span>
  </div>
</template>
<script>

import {mapActions} from 'vuex'

export default {
  name: "Privacy Policy",
  title: 'Privacy Policy',
  data: () => ({
    lastUpdated: "16th February 2023",
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
