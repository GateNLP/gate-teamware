(window.webpackJsonp=window.webpackJsonp||[]).push([[4],{344:function(e){e.exports=JSON.parse('{"current":"0.3.0","base":"/gate-teamware/0.3.0/","versions":[{"text":"0.3.0","value":"/gate-teamware/0.3.0/"},{"text":"development","value":"/gate-teamware/development/"}],"frontendSource":"../../../../frontend/src"}')},353:function(e,t,n){},381:function(e,t,n){"use strict";n(353)},399:function(e,t,n){"use strict";n(372);var a=n(374),i=n(400),o=n(401),s=n(366),r=n(344),l={name:"VersionSelector",data:function(){return{currentVersion:r.base}},computed:{versionOptions:function(){return r.versions}},methods:{versionChangeHandler:function(e){document.location.href=e}}},c=n(53);function u(e,t){return e.ownerDocument.defaultView.getComputedStyle(e,null)[t]}var d={name:"Navbar",components:{VersionSelector:Object(c.a)(l,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticStyle:{"font-weight":"bold !important"}},[n("b-select",{attrs:{options:e.versionOptions},on:{change:e.versionChangeHandler},model:{value:e.currentVersion,callback:function(t){e.currentVersion=t},expression:"currentVersion"}})],1)}),[],!1,null,"6e9385e6",null).exports,SidebarButton:o.a,NavLinks:s.a,SearchBox:i.a,AlgoliaSearchBox:a.a},data:function(){return{linksWrapMaxWidth:null}},computed:{algolia:function(){return this.$themeLocaleConfig.algolia||this.$site.themeConfig.algolia||{}},isAlgoliaSearch:function(){return this.algolia&&this.algolia.apiKey&&this.algolia.indexName}},mounted:function(){var e=this,t=parseInt(u(this.$el,"paddingLeft"))+parseInt(u(this.$el,"paddingRight")),n=function(){document.documentElement.clientWidth<719?e.linksWrapMaxWidth=null:e.linksWrapMaxWidth=e.$el.offsetWidth-t-(e.$refs.siteName&&e.$refs.siteName.offsetWidth||0)};n(),window.addEventListener("resize",n,!1)}},h=(n(381),Object(c.a)(d,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("header",{staticClass:"navbar"},[n("SidebarButton",{on:{"toggle-sidebar":function(t){return e.$emit("toggle-sidebar")}}}),e._v(" "),n("RouterLink",{staticClass:"home-link",attrs:{to:e.$localePath}},[e.$site.themeConfig.logo?n("img",{staticClass:"logo",attrs:{src:e.$withBase(e.$site.themeConfig.logo),alt:e.$siteTitle}}):e._e(),e._v(" "),e.$siteTitle?n("span",{ref:"siteName",staticClass:"site-name",class:{"can-hide":e.$site.themeConfig.logo}},[e._v(e._s(e.$siteTitle))]):e._e()]),e._v(" "),n("div",{staticClass:"links",style:e.linksWrapMaxWidth?{"max-width":e.linksWrapMaxWidth+"px"}:{}},[e.isAlgoliaSearch?n("AlgoliaSearchBox",{attrs:{options:e.algolia}}):!1!==e.$site.themeConfig.search&&!1!==e.$page.frontmatter.search?n("SearchBox"):e._e(),e._v(" "),n("NavLinks",{staticClass:"can-hide"}),e._v(" "),n("VersionSelector")],1)],1)}),[],!1,null,null,null));t.a=h.exports}}]);