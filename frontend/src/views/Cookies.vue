<template>
  <div class="container">

    <h1>Cookies policy</h1>
    <p>To make Teamware work properly, we place small data files called cookies on your device.</p>

    <h2>What are cookies?</h2>
    <p>
      Cookies are small data files that are placed on your computer or mobile device when you visit a website. Cookies are widely used by website owners in order to make their websites work, or to work more efficiently, as well as to provide reporting information.
      Cookies set by the website owner (in this case, Teamware) are called “first-party cookies.” Cookies set by parties other than the website owner are called “third-party cookies.” Third-party cookies enable third-party features or functionality to be provided on or through the website (e.g., advertising, interactive content, and analytics). The parties that set these third-party cookies can recognize your computer both when it visits the website in question and also when it visits certain other websites.
    </p>
    <h2>How do we use cookies?</h2>
    <p>Teamware exclusively uses cookies which are essential for the operation of the site and your security. Without the use of these cookies, you will not be able to use any features of the site which requires logging in.</p>

    <b-table :items="cookiesList">
    </b-table>

    <h2>How can you manage cookies?</h2>
    <h3>Removing cookies from your device</h3>
    <p>You can delete all cookies that are already on your device by clearing the browsing history of your browser. This will remove all cookies from all websites you have visited.</p>
    <p>Be aware though that you may also lose some saved information (e.g. saved login details, site preferences).</p>

    <h3>Managing site-specific cookies</h3>
    <p>For more detailed control over site-specific cookies, check the privacy and cookie settings in your preferred browser</p>

    <h3>Blocking cookies</h3>
    <p>You can set most modern browsers to prevent any cookies being placed on your device, but you may then have to manually adjust some preferences every time you visit a site/page. And some services and functionalities may not work properly at all (e.g. profile logging-in).</p>


  </div>
</template>

<script>
export default {
  name: "Cookies",
  data(){
    return {
      cookiesList: [
        {
          name: "csrftoken",
          service: "Teamware",
          purpose: "Used to avoid Cross-site attacks.",
          cookie_type_and_duration: "First-party session cookie, deleted after you quit your browser"
        },
        {
          name: "sessionid",
          service: "Teamware",
          purpose: "Identifies your session after you have logged in.",
          cookie_type_and_duration: "First-party session cookie. It is set when logging in and expires in 2 weeks or after logging out of the service."
        }
      ]
    }

  }

}
</script>

<style scoped>

</style>
