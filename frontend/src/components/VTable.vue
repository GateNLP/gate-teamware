<template>
  <div v-if="numRows > 0">
    <div class="row" v-if="showSearchBar">
      <div class="col">
        <div class="input-group mb-2">
          <div class="input-group-prepend">
            <label class="input-group-text">
              <i class="bi-search"></i>
            </label>
          </div>
          <input class="form-control" type="text" v-model="searchInput" placeholder="Search this table...">
          <button type="button" class="btn bg-transparent" style="margin-left: -41px; z-index: 100;"
                  @click="searchInput = null">
            <i class="bi-x-circle-fill"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="table-responsive">
      <table class="table table-hover table-striped">
        <thead>
        <tr>
          <th v-if="showRowNum"><a href="#" @click.prevent="changeColumnSort(null)">#</a></th>
          <th scope="col" v-for="colSpec in columnSpecs">
            <a v-if="colSpec.sortable" :class="{'text-success': colSpec.name === sortColumn}" href="#"
               @click.prevent="changeColumnSort(colSpec.name)">
              <span v-if="colSpec.title">{{ colSpec.title }}</span>
              <span v-else>{{ colSpec.name }}</span>
              <svg v-if="colSpec.name === sortColumn && !sortAsc" width="1em" height="1em" viewBox="0 0 16 16"
                   class="bi bi-arrow-up-short"
                   fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                      d="M8 12a.5.5 0 0 0 .5-.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5a.5.5 0 0 0 .5.5z"/>
              </svg>
              <svg v-if="colSpec.name === sortColumn && sortAsc" width="1em" height="1em" viewBox="0 0 16 16"
                   class="bi bi-arrow-down-short"
                   fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                      d="M8 4a.5.5 0 0 1 .5.5v5.793l2.146-2.147a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-3-3a.5.5 0 1 1 .708-.708L7.5 10.293V4.5A.5.5 0 0 1 8 4z"/>
              </svg>
            </a>
            <template v-else>
              <span v-if="colSpec.title">{{ colSpec.title }}</span>
              <span v-else>{{ colSpec.name }}</span>
            </template>
          </th>
        </tr>
        </thead>
        <tbody v-if="numFilteredRows > 0">
        <tr v-for="(n, offset) in pageEndIndex - pageStartIndex"
            :key="getRowKey(filteredData[pageStartIndex + offset])">
          <td v-if="showRowNum" class="text-secondary">{{ pageStartIndex + offset }}</td>
          <td v-for="colSpec in columnSpecs" :key="colSpec.name">
            <div v-if="colSpec.type === 'slot'">
              <slot :name="colSpec.name" :value="filteredData[pageStartIndex + offset]"></slot>
            </div>
            <div v-else>
              <router-link v-if="defaultFieldRendererHyperlinkFunc"
                           :to="defaultFieldRendererHyperlinkFunc(filteredData[pageStartIndex + offset])">
                <span v-html="renderField(colSpec, filteredData[pageStartIndex + offset])"></span>
              </router-link>
              <span v-else v-html="renderField(colSpec, filteredData[pageStartIndex + offset])"></span>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <div class="row">
      <div class="col-9">
        <ul class="pagination">
          <li class="page-item">
            <a v-if="pageIndex > 0" class="page-link" href="#" @click.prevent="changePage(pageIndex-1)">Prev</a>
            <span v-else class="page-link disabled text-secondary">Prev</span>
          </li>
          <li v-for="(n, page) in numPages" :class="{'page-item': true, 'active': page == pageIndex}">
            <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
          </li>
          <li class="page-item">
            <a v-if="pageIndex < numPages -1" class="page-link" href="#"
               @click.prevent="changePage(pageIndex+1)">Next</a>
            <span v-else class="page-link disabled text-secondary">Next</span>
          </li>
        </ul>
      </div>
      <div class="col-3 text-right">
        <div class="form-inline">
          <div class="label mr-1">Page size</div>
          <select class="form-control" v-model="rowsPerPage">
            <option value="10">10</option>
            <option value="50">50</option>
            <option value="100">100</option>
            <option :value="numRows">All</option>
          </select>

        </div>


      </div>
    </div>

    <button v-if="allowExport" class="btn btn-primary" @click="exportCsv()">
      <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-download" fill="currentColor"
           xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd"
              d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
        <path fill-rule="evenodd"
              d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
      </svg>
      Export CSV

    </button>
  </div>
</template>

<script>
import _ from 'lodash'
import Papa from 'papaparse'
// import moment from 'moment'

export default {
  name: "VTable",
  components: {},
  data() {
    return {
      localData: [],
      pageIndex: 0, //Current page
      sortColumn: null,
      sortAsc: true,
      rowsPerPage: 10,
      searchInput: null
    }
  },
  props: {
    /**
     * Table data in the form of array of objects with named properties e.g.
     *
     * [
     *  {
     *    id: 1,
     *    prop1: "Prop 1 string",
     *    prop2: "Prop 2 string",
     *  },
     *  ...
     * ]
     **/
    data: {
      type: Array,
      default() {
        return [];
      }
    },
    /**
     * An ordered dict of column name and type
     * {
     *  columnName : type,
     *  ...
     * }
     *
     * If type is slot, a custom slot in the name of of the column can be used with value as key, e.g. if
     * column name is prop3:
     *
     * <template v-slot:prop3="{ value }">My custom code - {{value.prop3}}</template>
     */
    columnDisplay: {
      type: Object,
      default() {
        return {};
      }
    },
    /**
     * A list of column names to ignore.
     * */
    columnIgnore: {
      type: Array,
      default() {
        return []
      }
    },
    /**
     * Allows exact specification of columns. The columnDisplay and columnIgnore is ignored if this
     * property is set.
     *
     * Input is an array of column specification in the order to be displayed, for example:
     *
     * [
     *  {
     *    name: "col_name", // The name of the field in the data object
     *    type: string|"slot", // The string of corresponding python type e.g. int, float, str. slot
     *                         // allows user to define their own custom renderer as a slot:
     *                         // <template v-slot:col_name="{ value }"></template>
     *                         // the value variable has the object of the current row.
     *    title: string, // The string to display as a column
     *    sortable: bool, // Allows column to be sortable
     *    sort_string_func, // Provide a custom function that returns a string which is used to sort the column,
     *                      // makes column sortable by default
     *    searchable: bool, // Allows column to be text searched, defaults to true if search_string_func is provided
     *    search_string_func: function, // Provide a custom function that returns
     *                                  // searchable string in that column, makes column searchable by default
     *  },
     *
     * ]
     *
     * If type is slot, a custom slot in the name of of the column can be used with value as key, e.g. if
     * column name is prop3:
     *
     * <template v-slot:prop3="{ value }">My custom code - {{value.prop3}}</template>
     */
    columns: {
      type: Array,
      default: null
    },
    /**
     * The name of the column used for indexing element in the table
     */
    index_column: {
      type: String,
      default: null
    },
    /**
     * Shows an additional 'rows' number column
     */
    showRowNum: {
      type: Boolean,
      default: true
    },
    defaultFieldRendererHyperlinkFunc: {
      type: Function,
      default: null,
    },
    showSearchBar: {
      type: Boolean,
      default: true
    },
    allowExport: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    numRows() { //Num of rows in the BASE data
      if (!this.localData)
        return 0;

      return this.localData.length;
    },
    columnSpecs() {

      let colNames = this.localData ? Object.keys(this.localData[0]) : [];
      let colNamesSet = new Set(colNames)

      if (this.columns) {
        // User has provided their own column spec
        let outputSpecs = _.cloneDeep(this.columns)
        for (let i in outputSpecs) {
          if (!("sortable" in outputSpecs[i])) {
            // If user hasn't overridden the sortable property
            // make columns that does not exist if data  or sort string not provided
            let colName = outputSpecs[i].name
            outputSpecs[i]["sortable"] = colNamesSet.has(colName) || "sort_string_func" in outputSpecs[i]
          }

          if (!("searchable" in outputSpecs[i])) {
            // If user hasn't overridden the searchable property
            // make columns that does not exist in data or search string not provided
            let colName = outputSpecs[i].name
            outputSpecs[i]["searchable"] = colNamesSet.has(colName) || "search_string_func" in outputSpecs[i]
          }
        }
        return outputSpecs
      } else if (this.numRows > 0) {
        //Only data is provided or used in combination with columnIgnore and columnDisplay
        let outputSpecs = []

        const ignoreSet = new Set(this.columnIgnore);

        for (let colName of colNames) {
          if (!ignoreSet.has(colName)) {
            const colType = colName in this.columnDisplay ? this.columnDisplay[colName] : null
            outputSpecs.push(
                {
                  name: colName,
                  type: colType,
                  sortable: true,
                  searchable: true,
                }
            )
          }
        }
        return outputSpecs
      }

      return []
    },
    filteredData() {
      let searchedData = []

      const colSpec = this.columnSpecs

      if (this.searchInput == null || this.searchInput.trim().length < 1) {
        // If no search string or is empty
        searchedData = this.localData
      } else {
        // Perform table search
        let searchString = this.searchInput.trim().toLowerCase()
        for (const i in this.localData) {
          const o = this.localData[i]

          for (const colSpec of this.columnSpecs) {

            if (colSpec.searchable) {
              //Only search in searchable columns

              if (colSpec.search_string_func) {
                // If user has defined a custom search string generator
                const customFieldString = colSpec.search_string_func(o)
                if (customFieldString && customFieldString.trim().toLowerCase().includes(searchString)) {
                  searchedData.push(o)
                  break
                }
              } else {
                //Convert object to string and search
                if (colSpec.name in o && String(o[colSpec.name]).trim().toLowerCase().includes(searchString)) {
                  searchedData.push(o)
                  break;
                }
              }
            }
          }

        }
      }

      if (!this.sortColumn)
        return searchedData;

      let sortType = ["asc"];
      if (!this.sortAsc)
        sortType = ["desc"];


      const sortCol = [this.sortColumn];

      //Prepare data for search
      for (const i in searchedData) {
        let o = searchedData[i]

        for (const colSpec of this.columnSpecs) {
          if (colSpec.sort_string_func) {
            o[colSpec.name] = colSpec.sort_string_func(o)
          }
        }
      }

      return _.orderBy(searchedData, sortCol, sortType);
    },
    numFilteredRows() {
      if (!this.filteredData) return 0;

      return this.filteredData.length;

    },
    numPages() {
      if (!this.localData) return 0;

      return Math.ceil(this.numFilteredRows / this.rowsPerPage)
    },
    pageStartIndex() {

      return this.pageIndex * this.rowsPerPage;

    },
    pageEndIndex() {
      let endIndex = ((this.pageIndex + 1) * this.rowsPerPage);
      if (endIndex > this.numFilteredRows) {
        endIndex = this.numFilteredRows;
      }
      return endIndex;
    },

  },
  methods: {
    changePage(page) {
      if (page < this.numPages && page >= 0)
        this.pageIndex = page;
    },
    changeColumnSort(colName) {
      if (!colName) {
        this.sortColumn = null;
        this.sortAsc = true;
        return;
      }

      if (colName == this.sortColumn) {
        if (this.sortAsc) {
          this.sortAsc = false
        } else {
          this.sortColumn = null;
          this.sortAsc = true;
        }
      } else {
        this.sortColumn = colName;
        this.sortAsc = true;

      }

    },
    exportCsv() {

      let text = Papa.unparse(this.filteredData);
      let filename = "data.csv";
      let element = document.createElement('a');
      element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(text));
      element.setAttribute('download', filename);
      element.style.display = 'none';
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);


    },
    makeid(length) {
      var result = '';
      var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      var charactersLength = characters.length;
      for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
      }
      return result;
    },
    getRowKey(rowObj) {
      if (this.index_column) {
        return rowObj[this.index_column]
      } else if ("id" in rowObj) {
        return rowObj["id"]
      } else {
        return this.makeid(30)
      }

    },
    renderField(colSpec, rowObj) {
      let outVal = rowObj[colSpec.name]
      if (colSpec.type === "datetime") {
        outVal = this.$options.filters.displayDatetime(outVal)

      } else if (colSpec.type === "float") {
        outVal = this.$options.filters.decimals(outVal, 3)
      }

      return outVal

    },
  },
  watch: {
    data: {
      immediate: true,
      handler(dataVal) {
        this.localData = _.cloneDeep(dataVal)
      }
    }
  },

}
</script>

<style scoped>

</style>
