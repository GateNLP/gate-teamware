<template>
  <div id="footer">
    <div>
      <b-navbar type="light" variant="light" toggleable="md" fixed="bottom">
        <b-navbar-nav align="right" :small=true>
          <b-nav-text>v{{ appVersion }}</b-nav-text>
          <b-nav-item href="https://github.com/GATENLP/gate-teamware" target="_blank">
            Source Code
            <b-icon-box-arrow-up-right
                  style="position: relative; font-size: 0.8em; padding-bottom: 0.2em;"></b-icon-box-arrow-up-right>
          </b-nav-item>
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
