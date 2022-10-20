<template>
  <div class="about container">
    <h1>About GATE Teamware</h1>

    <p>
    <h2>Using Teamware</h2>
    Teamware is developed by the <a href="https://gate.ac.uk" target="_blank">GATE team</a>, an academic research group at The University of Sheffield.
    As a result, future funding relies on evidence of the impact that the software provides.
    If you use Teamware, please let us know using the contact form at <a href = "https://gate.ac.uk/g8/contact" target="_blank">gate.ac.uk</a>.
    Please include details on grants, publications, commercial products etc. Any information that can help us to secure future funding for our work is greatly appreciated.
    </p>

    <p>
    <h3>Citation</h3>
    For published work that has used Teamware, please cite the <a href="https://github.com/GATENLP/gate-teamware" target="_blank">project's GitHub repository</a>. One way is to include a citation such as:
    </p>

    <p>
    <blockquote>
      Karmakharm, T., Wilby, D., Roberts, I., & Bontcheva, K. (2022). GATE Teamware (Version {{ appVersion }}) [Computer software]. https://github.com/GateNLP/gate-teamware
    </blockquote>
      </p>

    Please use the <b>Cite this repository</b> button at the top of the <a href="https://github.com/GATENLP/gate-teamware" target="_blank">project's GitHub repository</a> to get an up to date citation.

    <p>
    <h3>Version</h3>
    This is Teamware version {{ appVersion }}.
    </p>

  </div>
</template>
<script>
import {toastError} from "@/utils";
import JSRPCClient from '../jrpc';
import {version} from '../../../package.json'

export default {
  name: "Annotate",
  title: 'About',
  data: () => ({
    appVersion: version
  }),
  methods:{

  }


}
</script>
