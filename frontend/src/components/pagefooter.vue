<template>
  <div id="footer">
    <div>
      <b-navbar type="light" variant="light" toggleable="md" fixed="bottom">
        <b-navbar-nav align="right" :small=true>
          <b-nav-text>v{{ appVersion }}</b-nav-text>
          <b-nav-item to="/privacypolicy">Privacy Policy</b-nav-item>
          <b-nav-item to="/cookies">Cookies Policy</b-nav-item>
          <b-nav-item to="/terms">Terms & Conditions</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>
        </b-navbar-nav>
      </b-navbar>
    </div>
  </div>
</template>
<script>

import {version} from '../../../package.json'

export default {
  data: () => ({
    appVersion: version
  }),
}
</script>

<style>
</style>
