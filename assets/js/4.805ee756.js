(window.webpackJsonp=window.webpackJsonp||[]).push([[4],{357:function(t,n,e){},389:function(t,n,e){"use strict";e(357)},394:function(t,n,e){"use strict";e.r(n);var a=e(386),i=(e(387),e(88),e(193),e(194),e(335),e(54),e(336),{name:"InputErrorDisplay",props:["state","msgError","msgSuccess"],computed:{errorMessage:function(){return this.msgError?this.msgError:"Annotation required."},successMessage:function(){return this.msgSuccess?this.msgSuccess:"Annotation valid."}}}),s=e(53),o=Object(s.a)(i,(function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("div",[t._t("default"),t._v(" "),e("b-form-invalid-feedback",{attrs:{state:t.state}},[t._v("\n    "+t._s(t.errorMessage)+"\n  ")]),t._v(" "),e("b-form-valid-feedback",{attrs:{state:t.state}},[t._v("\n    "+t._s(t.successMessage)+"\n  ")])],2)}),[],!1,null,"3d308658",null).exports,r={name:"TextInput",components:{InputErrorDisplay:o},props:["value","config","state","msgError","msgSuccess"],computed:{inputVal:{get:function(){return this.value},set:function(t){this.$emit("input",t)}}},methods:{validate:function(){return!0}}},u=Object(s.a)(r,(function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("InputErrorDisplay",{attrs:{state:t.state,"msg-error":t.msgError,"msg-success":t.msgSuccess}},[e("BInput",{attrs:{name:t.config.name,state:t.state},model:{value:t.inputVal,callback:function(n){t.inputVal=n},expression:"inputVal"}})],1)}),[],!1,null,"6fd3e750",null).exports,c={name:"TextareaInput",components:{InputErrorDisplay:o},props:["value","config","state","msgError","msgSuccess"],computed:{inputVal:{get:function(){return this.value},set:function(t){this.$emit("input",t)}}}},l=Object(s.a)(c,(function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("InputErrorDisplay",{attrs:{state:t.state,"msg-error":t.msgError,"msg-success":t.msgSuccess}},[e("BTextarea",{attrs:{name:t.config.name,state:t.state},model:{value:t.inputVal,callback:function(n){t.inputVal=n},expression:"inputVal"}})],1)}),[],!1,null,"b283bc9e",null).exports;function p(t){var n=[];for(var e in t)n.push({value:e,text:t[e]});return n}var m={name:"RadioInput",components:{InputErrorDisplay:o},props:["value","config","state","msgError","msgSuccess"],computed:{options:function(){return this.config&&this.config.options?p(this.config.options):null},inputVal:{get:function(){return this.value},set:function(t){this.$emit("input",t)}}}},f=Object(s.a)(m,(function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("InputErrorDisplay",{attrs:{state:t.state,"msg-error":t.msgError,"msg-success":t.msgSuccess}},[e("b-form-radio-group",{attrs:{name:t.config.name,options:t.options,state:t.state},model:{value:t.inputVal,callback:function(n){t.inputVal=n},expression:"inputVal"}})],1)}),[],!1,null,"6069a453",null).exports,d={name:"CheckboxInput",components:{InputErrorDisplay:o},props:["value","config","state","msgError","msgSuccess"],computed:{options:function(){return this.config&&this.config.options?p(this.config.options):null},inputVal:{get:function(){return this.value},set:function(t){this.$emit("input",t)}}}},g=Object(s.a)(d,(function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("InputErrorDisplay",{attrs:{state:t.state,"msg-error":t.msgError,"msg-success":t.msgSuccess}},[e("b-form-checkbox-group",{attrs:{name:t.config.name,options:t.options,state:t.state},model:{value:t.inputVal,callback:function(n){t.inputVal=n},expression:"inputVal"}})],1)}),[],!1,null,"144c7291",null).exports,h={name:"SelectorInput",components:{InputErrorDisplay:o},props:["value","config","state","msgError","msgSuccess"],computed:{options:function(){return this.config&&this.config.options?p(this.config.options):null},inputVal:{get:function(){return this.value},set:function(t){this.$emit("input",t)}}}},v=Object(s.a)(h,(function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("InputErrorDisplay",{attrs:{state:t.state,"msg-error":t.msgError,"msg-success":t.msgSuccess}},[e("BFormSelect",{attrs:{options:t.options,state:t.state,name:t.config.name},model:{value:t.inputVal,callback:function(n){t.inputVal=n},expression:"inputVal"}})],1)}),[],!1,null,"af0192d6",null).exports,b=e(388),_={name:"HtmlDisplay",props:["config","document"],computed:{htmlDisplay:function(){try{if(this.config&&this.config.text){var t={};return this.document&&(t=this.document),b.render(this.config.text,t)}}catch(t){console.log(t)}return""}}},x={name:"AnnotationRenderer",components:{TextInput:u,TextareaInput:l,RadioInput:f,CheckboxInput:g,SelectorInput:v,HtmlDisplay:Object(s.a)(_,(function(){var t=this.$createElement;return(this._self._c||t)("div",{domProps:{innerHTML:this._s(this.htmlDisplay)}})}),[],!1,null,"55e0ebc2",null).exports},data:function(){return{annotationOutput:{},validation:{},validationErrorMsg:{},inputTypes:{text:"TextInput",textarea:"TextareaInput",radio:"RadioInput",checkbox:"CheckboxInput",selector:"SelectorInput",html:"HtmlDisplay"},ignoreValidateTypes:["html"],startTime:null}},props:{config:{default:null},document:{default:function(){return{text:"<p>Some html text <strong>in bold</strong>.</p><p>Paragraph 2.</p>"}}},allow_document_reject:{default:null}},methods:{startTimer:function(){this.startTime=new Date},getTimeElapsed:function(){return(new Date-this.startTime)/1e3},inputEventHandler:function(t){this.$emit("input",this.annotationOutput)},getInputType:function(t){return t in this.inputTypes?this.inputTypes[t]:null},generateValidationTracker:function(t){if(t){this.validation={};var n,e=Object(a.a)(t);try{for(e.s();!(n=e.n()).done;){var i=n.value;this.validation[i.name]=null}}catch(t){e.e(t)}finally{e.f()}}},validateAnnotation:function(){this.validation={},this.validationErrorMsg={};var t,n=Object(a.a)(this.config);try{for(n.s();!(t=n.n()).done;){var e=t.value,i=e.name,s=e.type;if(this.ignoreValidateTypes.includes(s)||e.optional&&("checkbox"!==s||!("minSelected"in e)))e.name in this.validation&&delete this.validation[i];else if(this.validation[i]=!1,i in this.annotationOutput&&this.valueNotEmpty(this.annotationOutput[i]))if("text"!==s&&"textarea"!==s||!("regex"in e))this.validation[i]="checkbox"!==s||!("minSelected"in e)||e.minSelected<=this.annotationOutput[i].length;else{var o=new RegExp(e.regex);this.validation[i]=o.test(this.annotationOutput[i])}}}catch(t){n.e(t)}finally{n.f()}var r=!0;for(var u in this.validation)this.ignoreValidateTypes.includes(u)||this.validation[u]||(r=!1);return r},valueNotEmpty:function(t){return"string"==typeof t&&t.length>0||t instanceof Array&&t.length>0},submitHandler:function(t){var n=this.getTimeElapsed(),e=this.validateAnnotation();this.$forceUpdate(),e&&(this.$emit("submit",this.annotationOutput,n),this.clearForm(),this.startTimer())},clearForm:function(){this.annotationOutput={},this.validation={}},clearFormHandler:function(t){this.clearForm()},rejectHandler:function(t){this.$emit("reject"),this.startTimer()}},watch:{config:{immediate:!0,handler:function(t){this.generateValidationTracker(t)}}},mounted:function(){this.startTimer()}},y={name:"AnnotationRendererPreview",components:{AnnotationRenderer:Object(s.a)(x,(function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("div",{staticClass:"annotation"},[t._l(t.config,(function(n){return e("div",{key:n.name},[e("b-form-group",{attrs:{label:n.title}},[n.description?e("p",{staticClass:"annotation-description"},[t._v(t._s(n.description))]):t._e(),t._v(" "),t.getInputType(n.type)?e(t.getInputType(n.type),{tag:"component",attrs:{name:n.name,config:n,document:t.document,state:t.validation[n.name],"msg-success":n.valSuccess,"msg-error":n.valError},on:{input:t.inputEventHandler},model:{value:t.annotationOutput[n.name],callback:function(e){t.$set(t.annotationOutput,n.name,e)},expression:"annotationOutput[elemConfig.name]"}}):e("div",[t._v("\n        Component invalid\n      ")])],1)],1)})),t._v(" "),e("b-row",[e("b-col",[e("BButton",{staticClass:"mr-4",attrs:{variant:"success"},on:{click:function(n){return n.preventDefault(),t.submitHandler.apply(null,arguments)}}},[t._v("Submit")]),t._v(" "),e("BButton",{staticClass:"mr-4",attrs:{variant:"warning"},on:{click:function(n){return n.preventDefault(),t.clearFormHandler.apply(null,arguments)}}},[t._v("Clear")]),t._v(" "),t.allow_document_reject?e("BButton",{attrs:{variant:"danger"},on:{click:function(n){return n.preventDefault(),t.rejectHandler.apply(null,arguments)}}},[t._v("Reject document")]):t._e()],1)],1)],2)}),[],!1,null,"bf4fb030",null).exports},data:function(){return{annotationOutput:{}}},props:{document:{default:function(){return{text:"Sometext with <strong>html</strong>"}}},config:{default:function(){return[{name:"htmldisplay",type:"html",text:"{{{text}}}"},{name:"sentiment",type:"radio",title:"Sentiment",description:"Please select a sentiment of the text above.",options:{negative:"Negative",neutral:"Neutral",positive:"Positive"}}]}}}},E=(e(389),Object(s.a)(y,(function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("div",[e("b-tabs",[e("b-tab",{attrs:{title:"Code"}},[t._t("default")],2),t._v(" "),e("b-tab",{attrs:{title:"Preview"}},[e("b-card",{staticClass:"mb-2 mt-2"},[e("AnnotationRenderer",{attrs:{config:t.config,document:t.document,allow_document_reject:!0},model:{value:t.annotationOutput,callback:function(n){t.annotationOutput=n},expression:"annotationOutput"}})],1),t._v(" "),e("b-card",{staticClass:"mb-2 mt-2"},[e("p",[e("strong",[t._v("Annotation output:")])]),t._v("\n        "+t._s(t.annotationOutput)+"\n      ")])],1)],1)],1)}),[],!1,null,null,null));n.default=E.exports}}]);