<template>
  <div class="about container">
    <h1>About GATE Teamware</h1>

    <h2>Using Teamware</h2>
    <p>
    Teamware is developed by the <a href="https://gate.ac.uk" target="_blank">GATE team</a>, an academic research group at The University of Sheffield.
    As a result, future funding relies on evidence of the impact that the software provides.
    If you use Teamware, please let us know using the contact form at <a href = "https://gate.ac.uk/g8/contact" target="_blank">gate.ac.uk</a>.
    Please include details on grants, publications, commercial products etc. Any information that can help us to secure future funding for our work is greatly appreciated.
    </p>

    <h3>Citation</h3>
    <p>
    For published work that has used Teamware, please cite the <a href="https://aclanthology.org/2023.eacl-demo.17/" target="_blank">EACL23 demo paper</a>. One way is to include a citation such as:
    </p>

    <p>
    <blockquote>
      Wilby, D., Karmakharm, T., Roberts, I., Song, X. & Bontcheva, K. (2023). GATE Teamware 2: An open-source tool for collaborative document classification annotation. In Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations, pages 145–151, Dubrovnik, Croatia. Association for Computational Linguistics. https://aclanthology.org/2023.eacl-demo.17/
    </blockquote>
      </p>

    <p>
      Please use the <b>Cite this repository</b> button at the top of the <a href="https://github.com/GATENLP/gate-teamware" target="_blank">project's GitHub repository</a> to get an up to date citation.
    </p>
    <p>
      Permanent references to each version of the software are available from <a href="https://doi.org/10.5281/zenodo.7899193">Zenodo</a>.
    </p>

    <h3>Version</h3>
    <p>
    This instance is running Teamware version {{ appVersion }}.
    </p>

    <h3>Source Code & Licensing</h3>
    <p>
      Teamware is free open source software available at the <a href="https://github.com/GATENLP/gate-teamware" target="_blank">project's GitHub repository</a> under the GNU Affero General Public License v3.
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
