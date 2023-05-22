(window.webpackJsonp=window.webpackJsonp||[]).push([[8],{264:function(t,e,n){},293:function(t,e,n){"use strict";n(264)},300:function(t,e,n){"use strict";n.r(e);n(93);var a={name:"InputErrorDisplay",props:["state","msgError","msgSuccess"],computed:{errorMessage(){return this.msgError?this.msgError:"Annotation required."},successMessage(){return this.msgSuccess?this.msgSuccess:"Annotation valid."}}},o=n(16),i=Object(o.a)(a,(function(){var t=this,e=t._self._c;return e("div",[t._t("default"),t._v(" "),e("b-form-invalid-feedback",{attrs:{state:t.state}},[t._v("\n    "+t._s(t.errorMessage)+"\n  ")]),t._v(" "),e("b-form-valid-feedback",{attrs:{state:t.state}},[t._v("\n    "+t._s(t.successMessage)+"\n  ")])],2)}),[],!1,null,"3d308658",null).exports,r={name:"TextInput",components:{InputErrorDisplay:i},props:["value","config","state","msgError","msgSuccess"],computed:{inputVal:{get(){return this.value},set(t){this.$emit("input",t)}}},methods:{validate:()=>!0}},s=Object(o.a)(r,(function(){var t=this,e=t._self._c;return e("InputErrorDisplay",{attrs:{state:t.state,"msg-error":t.msgError,"msg-success":t.msgSuccess}},[e("BInput",{attrs:{name:t.config.name,state:t.state},model:{value:t.inputVal,callback:function(e){t.inputVal=e},expression:"inputVal"}})],1)}),[],!1,null,"feeaac20",null).exports,l={name:"TextareaInput",components:{InputErrorDisplay:i},props:["value","config","state","msgError","msgSuccess"],computed:{inputVal:{get(){return this.value},set(t){this.$emit("input",t)}}}},u=Object(o.a)(l,(function(){var t=this,e=t._self._c;return e("InputErrorDisplay",{attrs:{state:t.state,"msg-error":t.msgError,"msg-success":t.msgSuccess}},[e("BTextarea",{attrs:{name:t.config.name,state:t.state},model:{value:t.inputVal,callback:function(e){t.inputVal=e},expression:"inputVal"}})],1)}),[],!1,null,"b556f86e",null).exports;function c(t,e,n="."){if(null==t||null==e||"string"!=typeof e||e.trim().length<1)return null;const a=e.trim().split(n);let o=t;for(let t in a){if(!(a[t]in o))return null;o=o[a[t]]}return o}function p(t,e){let n=[];if(Array.isArray(t))for(let a of t)if(e&&a&&"object"==typeof a&&"string"==typeof a.fromDocument){const t=a.fromDocument;let o=t in e?e[t]:c(e,t);if("string"==typeof o){const t="string"==typeof a.separator?a.separator:";";o=t?o.split(t):[o],o=o.map(t=>t.trim());const e="string"==typeof a.valueLabelSeparator?a.valueLabelSeparator:"=";e&&(o=o.map(t=>{const n=t.indexOf(e);return n>=0?{value:t.substring(0,n).trim(),label:t.substring(n+e.length).trim()}:t}))}n.push(...p(o))}else null!=a&&("string"==typeof a?n.push({value:a,text:a}):"value"in a&&n.push({value:a.value,text:"label"in a?a.label:a.value,helptext:"helptext"in a?a.helptext:null}));else for(let e in t)n.push({value:e,text:t[e]});return n}var m={name:"RadioInput",components:{InputErrorDisplay:i},props:["value","config","document","state","msgError","msgSuccess"],computed:{options(){return this.config&&this.config.options?p(this.config.options,this.document):null},inputVal:{get(){return this.value},set(t){this.$emit("input",t)}}}},h=Object(o.a)(m,(function(){var t=this,e=t._self._c;return e("InputErrorDisplay",{attrs:{state:t.state,"msg-error":t.msgError,"msg-success":t.msgSuccess,"label-cols":"3"}},[e("b-form-group",{attrs:{id:t.config.name}},t._l(t.options,(function(n,a){return e("b-form-radio",{key:n.value,attrs:{value:n.value,state:t.state,inline:"vertical"!==t.config.orientation,name:t.config.name},model:{value:t.inputVal,callback:function(e){t.inputVal=e},expression:"inputVal"}},[t._v("\n        "+t._s(n.text)+"\n        "),null!=n.helptext?e("b-icon-question-circle",{staticClass:"annotation-help-prompt",attrs:{id:t.config.name+"__opt"+a}}):t._e(),t._v(" "),null!=n.helptext?e("b-tooltip",{attrs:{target:t.config.name+"__opt"+a,title:n.helptext}}):t._e()],1)})),1)],1)}),[],!1,null,"ccbb4eaa",null).exports,d={name:"CheckboxInput",components:{InputErrorDisplay:i},props:["value","config","document","state","msgError","msgSuccess"],computed:{options(){return this.config&&this.config.options?p(this.config.options,this.document):null},inputVal:{get(){return this.value},set(t){this.$emit("input",t)}}}},f=Object(o.a)(d,(function(){var t=this,e=t._self._c;return e("InputErrorDisplay",{attrs:{state:t.state,"msg-error":t.msgError,"msg-success":t.msgSuccess}},[e("b-form-checkbox-group",{attrs:{stacked:"vertical"==t.config.orientation,name:t.config.name},model:{value:t.inputVal,callback:function(e){t.inputVal=e},expression:"inputVal"}},t._l(t.options,(function(n,a){return e("b-form-checkbox",{key:n.value,attrs:{value:n.value,state:t.state}},[t._v("\n      "+t._s(n.text)+"\n      "),null!=n.helptext?e("b-icon-question-circle",{staticClass:"annotation-help-prompt",attrs:{id:t.config.name+"__opt"+a}}):t._e(),t._v(" "),null!=n.helptext?e("b-tooltip",{attrs:{target:t.config.name+"__opt"+a,title:n.helptext}}):t._e()],1)})),1)],1)}),[],!1,null,"4fe134a3",null).exports,g={name:"SelectorInput",components:{InputErrorDisplay:i},props:["value","config","document","state","msgError","msgSuccess"],computed:{options(){return this.config&&this.config.options?p(this.config.options,this.document):null},inputVal:{get(){return this.value},set(t){this.$emit("input",t)}}}},v=Object(o.a)(g,(function(){var t=this,e=t._self._c;return e("InputErrorDisplay",{attrs:{state:t.state,"msg-error":t.msgError,"msg-success":t.msgSuccess}},[e("BFormSelect",{attrs:{options:t.options,state:t.state,name:t.config.name},model:{value:t.inputVal,callback:function(e){t.inputVal=e},expression:"inputVal"}})],1)}),[],!1,null,"c4d709ee",null).exports,_=n(287),b=n.n(_),y={name:"HtmlDisplay",props:["config","document"],computed:{htmlDisplay(){try{if(this.config&&this.config.text){let t={};return this.document&&(t=this.document),b.a.render(this.config.text,t)}}catch(t){console.log(t)}return""}}},x=Object(o.a)(y,(function(){return(0,this._self._c)("div",{domProps:{innerHTML:this._s(this.htmlDisplay)}})}),[],!1,null,"081ebbc0",null).exports;const w={Annotation:"Annotation",Test:"Test",Training:"Training"};var E={name:"MarkdownRenderer",props:{content:{default:""},options:{default:()=>({markdownIt:{html:!0}})}}},D=Object(o.a)(E,(function(){return(0,this._self._c)("markdown-it-vue",{attrs:{content:this.content,options:this.options}})}),[],!1,null,"e0913990",null).exports,k=n(288),A=n.n(k),T=(n(94),n(249)),I=n(289),S=n(290),V=n(291),C=n(292);function O(t,e){if(e.length>2)throw new Error(`At most two arguments expected for "${t}" quantifier`);let n,a,o;if(1===e.length)n=Symbol("x"),a=e[0],o={type:"Identifier",name:n};else{const i=e[0];if("BinaryExpression"!==i.type||"in"!==i.operator||"Identifier"!==i.left.type)throw new Error(`"${t}" quantifier binding must be of the form "identifier in expression"`);n=i.left.name,a=i.right,o=e[1]}return[n,a,o]}T.b.registerPlugin(I.a,S.a,V.a,C.a),T.b.addBinaryOp("in",6,(function(t,e){return!!e&&(Array.isArray(e)?e.includes(t):t in e)})),T.b.addBinaryOp("=~",4,(function(t,e){if(!(e instanceof RegExp))throw new Error("Right hand argument of =~ must be a regular expression");return e.test(t)})),T.b.prototype.evaluateMember=function(t){return this.eval(t.object,e=>this.evalSyncAsync(t.computed?this.eval(t.property):t.property.name,n=>{if("string"==typeof n&&/^\$|^(?:__proto__|prototype|constructor|__ob__)$/.test(n))throw Error(`Access to member "${n}" disallowed.`);return[e,(t.optional?e||{}:e)[n],n]}))},T.b.addEvaluator("Identifier",(function(t){const e=t.name;if("string"==typeof e&&/^\$|^(?:__proto__|prototype|constructor|__ob__)$/.test(e))throw Error(`Access to member "${e}" disallowed.`);return this.context[e]})),T.b.addEvaluator("CallExpression",(function(t){if("Identifier"!==t.callee.type)throw new Error("Illegal function call");switch(t.callee.name){case"all":return function(t,e){let[n,a,o]=O("all",e);return t.eval(a,e=>{if(!e)return!0;const a=Array.isArray(e);if(a||(e=Object.entries(e)),0===e.length)return!0;const i={...t.context};if(t.isAsync){const t=(r,s)=>(i[n]=a?r:{key:r[0],value:r[1]},T.b.evalAsync(o,i).then(n=>!!n&&(++s>=e.length||t(e[s],s))));return t(e[0],0)}return e.every(t=>(i[n]=a?t:{key:t[0],value:t[1]},T.b.eval(o,i)))})}(this,t.arguments);case"any":return function(t,e){let[n,a,o]=O("any",e);return t.eval(a,e=>{if(!e)return!1;const a=Array.isArray(e);if(a||(e=Object.entries(e)),0===e.length)return!1;const i={...t.context};if(t.isAsync){const t=(r,s)=>(i[n]=a?r:{key:r[0],value:r[1]},T.b.evalAsync(o,i).then(n=>!!n||!(++s>=e.length)&&t(e[s],s)));return t(e[0],0)}return e.some(t=>(i[n]=a?t:{key:t[0],value:t[1]},T.b.eval(o,i)))})}(this,t.arguments);default:throw new Error(`Unsupported function "${t.callee.name}"`)}}));var j={name:"AnnotationRenderer",components:{TextInput:s,TextareaInput:u,RadioInput:h,CheckboxInput:f,SelectorInput:v,HtmlDisplay:x,MarkdownRenderer:D},data:()=>({annotationData:{},validation:{},validationErrorMsg:{},inputTypes:{text:"TextInput",textarea:"TextareaInput",radio:"RadioInput",checkbox:"CheckboxInput",selector:"SelectorInput",html:"HtmlDisplay"},ignoreValidateTypes:["html"],startTime:null,DocumentType:w,answerBgColor:{},conditions:[],exceptions:{parse:[],evaluate:[]}}),props:{config:{default:null},document:{default:()=>({text:"<p>Some html text <strong>in bold</strong>.</p><p>Paragraph 2.</p>"})},document_type:{default:null},doc_gold_field:{default:"gold"},doc_preannotation_field:{default:""},allow_document_reject:{default:null},allow_cancel:{default:null},clear_after_submit:{default:!0,type:Boolean},show_expression_errors:{default:null}},computed:{preAnnotationValues(){return null!=this.document&&null!=this.doc_preannotation_field?c(this.document,this.doc_preannotation_field):null},shownElements(){return this.exceptions.evaluate=[],this.config?this.config.filter((t,e)=>{try{return this.conditions[e]({document:this.document,annotation:this.annotationData})}catch(e){return this.exceptions.evaluate.push({config:t,error:e}),!1}}):[]},annotationOutput(){const t={};for(const e of this.shownElements){const n=this.annotationData[e.name];null!=n&&(t[e.name]=n)}return t}},methods:{setAnnotationData(t){this.annotationData=t},startTimer(){this.startTime=new Date},getTimeElapsed(){if(this.document_type!=this.DocumentType.Annotation)return null;return(new Date-this.startTime)/1e3},inputEventHandler(t){this.$emit("input",this.annotationOutput)},getInputType(t){return t in this.inputTypes?this.inputTypes[t]:null},generateValidationTracker(t){if(t){const e=()=>!0;this.validation={},this.conditions=[],this.exceptions.parse=[];for(let n of t){this.validation[n.name]=null;let t=e;if(n.if)try{t=Object(T.a)(n.if)}catch(t){this.exceptions.parse.push({config:n,error:t})}this.conditions.push(t)}}},validateAnnotation(){this.validation={},this.validationErrorMsg={};for(let t of this.shownElements){const e=t.name,n=t.type;if(this.ignoreValidateTypes.includes(n)||t.optional&&("checkbox"!==n||!("minSelected"in t)))t.name in this.validation&&delete this.validation[e];else if(this.validation[e]=!1,e in this.annotationData&&this.valueNotEmpty(this.annotationData[e]))if("text"!==n&&"textarea"!==n||!("regex"in t))this.validation[e]="checkbox"!==n||!("minSelected"in t)||t.minSelected<=this.annotationData[e].length;else{const n=new RegExp(t.regex);this.validation[e]=n.test(this.annotationData[e])}}let t=!0;for(let e in this.validation)this.ignoreValidateTypes.includes(e)||this.validation[e]||(t=!1);return t},valueNotEmpty:t=>"string"==typeof t&&t.length>0||t instanceof Array&&t.length>0,submitHandler(t){let e=this.getTimeElapsed(),n=this.validateAnnotation();this.$forceUpdate(),n&&(this.$emit("submit",this.annotationOutput,e),this.clear_after_submit&&this.clearForm(),this.startTimer())},clearForm(){this.annotationData={},this.validation={},this.fillWithPreAnnotation()},clearFormHandler(t){this.clearForm()},rejectHandler(t){this.$emit("reject"),this.startTimer()},cancelHandler(t){this.$emit("cancel"),this.startTimer()},getAnswerBgColor(t){let e=this.annotationData[t.name],n=this.document[this.doc_gold_field][t.name].value;return Object.keys(t.options).includes(e)?e==n?"success":"danger":"Default"},showExplanation(t){return"html"!=t.type&&(this.document_type==w.Training&&null!==this.annotationData[t.name])},answerText(t){let e=this.annotationData[t.name],n=this.document[this.doc_gold_field][t.name].value;return null!==Object.keys(t.options)?e==n?"Correct! ✔️":"Incorrect ❌":""},fillWithPreAnnotation(){null!=this.preAnnotationValues&&this.setAnnotationData(A.a.cloneDeep(this.preAnnotationValues))}},watch:{config:{immediate:!0,handler(t){this.generateValidationTracker(t)}},document:{immediate:!0,handler(){this.fillWithPreAnnotation()}},doc_preannotation_field:{immediate:!0,handler(){this.fillWithPreAnnotation()}},annotationData:{immediate:!0,deep:!0,handler(){for(const t in this.config)this.showExplanation(this.config[t])&&(this.answerBgColor[this.config[t].name]=this.getAnswerBgColor(this.config[t]))}}},mounted(){for(const t in this.config)"html"!=this.config[t].type&&(this.answerBgColor[this.config[t].name]="Default");this.startTimer()}},B={name:"AnnotationRendererPreview",components:{AnnotationRenderer:Object(o.a)(j,(function(){var t=this,e=t._self._c;return e("div",{staticClass:"annotation"},[t._l(t.shownElements,(function(n){return e("div",{key:n.name},[e("b-form-group",{attrs:{label:n.title}},[n.description?e("p",{staticClass:"annotation-description"},[t._v(t._s(n.description))]):t._e(),t._v(" "),t.getInputType(n.type)?e(t.getInputType(n.type),{tag:"component",attrs:{name:n.name,config:n,document:t.document,state:t.validation[n.name],"msg-success":n.valSuccess,"msg-error":n.valError},on:{input:t.inputEventHandler},model:{value:t.annotationData[n.name],callback:function(e){t.$set(t.annotationData,n.name,e)},expression:"annotationData[elemConfig.name]"}}):e("div",[t._v("\n        Component invalid\n      ")]),t._v(" "),t.showExplanation(n)?e("b-card",{staticClass:"mb-4",attrs:{"border-variant":t.answerBgColor[n.name]}},[e("MarkdownRenderer",{attrs:{content:t.answerText(n)+"<br>"+t.document[t.doc_gold_field][n.name].explanation}})],1):t._e()],1)],1)})),t._v(" "),e("BRow",[e("b-col",[e("BButton",{staticClass:"mr-4",attrs:{variant:"success"},on:{click:function(e){return e.preventDefault(),t.submitHandler.apply(null,arguments)}}},[t._v("Submit")]),t._v(" "),e("BButton",{staticClass:"mr-4",attrs:{variant:"warning"},on:{click:function(e){return e.preventDefault(),t.clearFormHandler.apply(null,arguments)}}},[t._v("Clear")]),t._v(" "),t.allow_document_reject?e("BButton",{attrs:{variant:"danger"},on:{click:function(e){return e.preventDefault(),t.rejectHandler.apply(null,arguments)}}},[t._v("Reject document")]):t._e(),t._v(" "),t.allow_cancel?e("BButton",{attrs:{variant:"danger"},on:{click:function(e){return e.preventDefault(),t.cancelHandler.apply(null,arguments)}}},[t._v("Cancel")]):t._e()],1)],1),t._v(" "),t.show_expression_errors&&(t.exceptions.parse.length||t.exceptions.evaluate.length)?[e("b-card",{staticClass:"mt-3",attrs:{header:"Expression errors"}},[t._l(t.exceptions.parse,(function(n){return e("b-alert",{key:n.config.name,attrs:{variant:"danger",show:""}},[e("p",[e("strong",[t._v('Error parsing "if" expression for component "'+t._s(n.config.name)+'"')])]),t._v(" "),e("p",[t._v(t._s(n.error))])])})),t._v(" "),t._l(t.exceptions.evaluate,(function(n){return e("b-alert",{key:n.config.name,attrs:{variant:"warning",show:""}},[e("p",[e("strong",[t._v('Error evaluating "if" expression for component "'+t._s(n.config.name)+'"')])]),t._v(" "),e("p",[t._v(t._s(n.error))])])}))],2)]:t._e()],2)}),[],!1,null,"08438e66",null).exports},data:()=>({annotationOutput:{}}),props:{preAnnotation:{default:()=>""},document:{default:()=>({text:"Sometext with <strong>html</strong>"})},config:{default:()=>[{name:"htmldisplay",type:"html",text:"{{{text}}}"},{name:"sentiment",type:"radio",title:"Sentiment",description:"Please select a sentiment of the text above.",options:{negative:"Negative",neutral:"Neutral",positive:"Positive"}}]}}},$=(n(293),Object(o.a)(B,(function(){var t=this,e=t._self._c;return e("div",[e("b-tabs",[e("b-tab",{attrs:{title:"Code"}},[t._t("default")],2),t._v(" "),e("b-tab",{attrs:{title:"Preview"}},[e("b-card",{staticClass:"mb-2 mt-2"},[e("AnnotationRenderer",{attrs:{config:t.config,document:t.document,allow_document_reject:!0,doc_preannotation_field:t.preAnnotation},model:{value:t.annotationOutput,callback:function(e){t.annotationOutput=e},expression:"annotationOutput"}})],1),t._v(" "),e("b-card",{staticClass:"mb-2 mt-2"},[e("p",[e("strong",[t._v("Annotation output:")])]),t._v("\n        "+t._s(t.annotationOutput)+"\n      ")])],1)],1)],1)}),[],!1,null,null,null));e.default=$.exports}}]);