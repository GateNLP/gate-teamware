(window.webpackJsonp=window.webpackJsonp||[]).push([[3],{246:function(e){e.exports=JSON.parse('{"current":"2.0.0","base":"/gate-teamware/2.0.0/","versions":[{"text":"0.3.0","value":"/gate-teamware/0.3.0/"},{"text":"0.4.0","value":"/gate-teamware/0.4.0/"},{"text":"2.0.0","value":"/gate-teamware/2.0.0/"},{"text":"development","value":"/gate-teamware/development/"}],"frontendSource":"../../../../frontend/src"}')},255:function(e,t,a){},277:function(e,t,a){"use strict";a(255)},292:function(e,t,a){"use strict";var i=a(271),n=a(293),s=a(294),o=a(268),r=a(246),l={name:"VersionSelector",data:()=>({currentVersion:r.base}),computed:{versionOptions:()=>r.versions},methods:{versionChangeHandler(e){document.location.href=e}}},c=a(16);function h(e,t){return e.ownerDocument.defaultView.getComputedStyle(e,null)[t]}var u={name:"Navbar",components:{VersionSelector:Object(c.a)(l,(function(){var e=this,t=e._self._c;return t("div",{staticStyle:{"font-weight":"bold !important"}},[t("b-select",{attrs:{options:e.versionOptions},on:{change:e.versionChangeHandler},model:{value:e.currentVersion,callback:function(t){e.currentVersion=t},expression:"currentVersion"}})],1)}),[],!1,null,"3e34425f",null).exports,SidebarButton:s.a,NavLinks:o.a,SearchBox:n.a,AlgoliaSearchBox:i.a},data:()=>({linksWrapMaxWidth:null}),computed:{algolia(){return this.$themeLocaleConfig.algolia||this.$site.themeConfig.algolia||{}},isAlgoliaSearch(){return this.algolia&&this.algolia.apiKey&&this.algolia.indexName}},mounted(){const e=parseInt(h(this.$el,"paddingLeft"))+parseInt(h(this.$el,"paddingRight")),t=()=>{document.documentElement.clientWidth<719?this.linksWrapMaxWidth=null:this.linksWrapMaxWidth=this.$el.offsetWidth-e-(this.$refs.siteName&&this.$refs.siteName.offsetWidth||0)};t(),window.addEventListener("resize",t,!1)}},d=(a(277),Object(c.a)(u,(function(){var e=this,t=e._self._c;return t("header",{staticClass:"navbar"},[t("SidebarButton",{on:{"toggle-sidebar":function(t){return e.$emit("toggle-sidebar")}}}),e._v(" "),t("RouterLink",{staticClass:"home-link",attrs:{to:e.$localePath}},[e.$site.themeConfig.logo?t("img",{staticClass:"logo",attrs:{src:e.$withBase(e.$site.themeConfig.logo),alt:e.$siteTitle}}):e._e(),e._v(" "),e.$siteTitle?t("span",{ref:"siteName",staticClass:"site-name",class:{"can-hide":e.$site.themeConfig.logo}},[e._v(e._s(e.$siteTitle))]):e._e()]),e._v(" "),t("div",{staticClass:"links",style:e.linksWrapMaxWidth?{"max-width":e.linksWrapMaxWidth+"px"}:{}},[e.isAlgoliaSearch?t("AlgoliaSearchBox",{attrs:{options:e.algolia}}):!1!==e.$site.themeConfig.search&&!1!==e.$page.frontmatter.search?t("SearchBox"):e._e(),e._v(" "),t("NavLinks",{staticClass:"can-hide"}),e._v(" "),t("VersionSelector")],1)],1)}),[],!1,null,null,null));t.a=d.exports}}]);