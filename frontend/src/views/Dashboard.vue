<template>
  <!-- <div class="justify-content-center align-items-center vh-100"> -->
    <div class="justify-content-center align-items-center">
    <CCard style="margin-top: 100px;">
    <CCardBody>
      <div class="datatable-container">
        <CForm style="margin-bottom: 15px;">
          <CRow>
            <CCol xs="12" md="4">
                <CInput
                  type="date"
                  id="fromDate"
                  placeholder="dd-mm-yyyy" value=""
                  min="1997-01-01" max="2030-12-31"
                  v-model="fromDate"
                  label="From Date"
                />
            </CCol>
            <CCol xs="12" md="4">
                <CInput
                  type="date"
                  id="toDate"
                  placeholder="dd-mm-yyyy" value=""
                  min="1997-01-01" max="2030-12-31"
                  v-model="toDate"
                  label="To Date"
                />
            </CCol>
            <CCol xs="12" md="4">
                <CInput
                  type="text"
                  id="portfolioNumber"
                  v-model="portfolioNumber"
                  label="Portfolio Number"
                />
            </CCol>
          </CRow>
          <CRow>
            <CCol xs="12" md="4">
                <CInput
                  type="text"
                  id="shareSymbol"
                  v-model="shareSymbol"
                  label="Share Symbol"
                />
            </CCol>

            <CCol xs="12" md="4">
                <CInput
                  type="text"
                  id="securityCurrency"
                  v-model="securityCurrency"
                  label="Security Currency"
                />
            </CCol>
          </CRow>

          <CRow>
            <CCol xs="12" md="8" class="text-right">

            </CCol>

            <CCol xs="12" md="2" class="text-right">
              <CButton
                color="primary" @click="fetchData">
                Apply
              </CButton>
            </CCol>

            <CCol xs="12" md="2" class="text-left">
              <CButton color="success" class="mr-1" @click="generatePdf">
                Print
              </CButton>
            </CCol>
          </CRow>
        </CForm>
        
        <CInput
          v-model="filterValue"
          placeholder="Filter by name"
          class="mb-3"
        />
        <!-- <p>Items count: {{ totalRecords }}</p> -->
        <CDataTable
          ref="dataTable"
          :items="items"
          :fields="fields"
          columnFilter
          items-per-page-select
          :items-per-page="10"
          hover
          sorter
          pagination
          :tableFilterValue="filterValue"
          @table-filter="onFilter"
          striped
          bordered
          responsive
        >
          <template #cell(TRADE_DATE)="data">
            {{ formatDate(data.item.TRADE_DATE) }}
          </template>
          <template #cell(PRICE)="data">
            {{ formatNumber(data.item.PRICE) }}
          </template>
          <template #cell(NET_AMT_TRADE)="data">
            {{ formatNumber(data.item.NET_AMT_TRADE) }}
          </template>
          <template #cell(BROKER_COMMS)="data">
            {{ formatNumber(data.item.BROKER_COMMS) }}
          </template>
          <template #cell(PROF_LOSS_SEC_CCY)="data">
            {{ formatNumber(data.item.PROF_LOSS_SEC_CCY) }}
          </template>
          
        </CDataTable>
      </div>
    </CCardBody>
    </CCard>
  </div>
</template>


<script>
import axios from 'axios';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

export default {
  data() {
    return {
      items: [],
      fields: [
        { key: 'TRADE_DATE', label: 'Trade Date', sorter: true, filter: true },
        { key: 'SECURITY_ACCOUNT', label: 'Security Account', sorter: true, filter: true },
        { key: 'SAM_NAME', label: 'Account Name', sorter: true, filter: true },
        { key: 'SECURITY_NUMBER', label: 'Security Number', sorter: true, filter: true },
        { key: 'SECURITY_NAME', label: 'Security Name', sorter: true, filter: true },
        { key: 'TRANS_TYPE', label: 'Transaction Type', sorter: true, filter: true },
        { key: 'RECID', label: 'RECID', sorter: true, filter: true },
        { key: 'NO_NOMINAL', label: 'No Nominal', sorter: true, filter: true },
        { key: 'PRICE', label: 'Price', sorter: true, filter: true },
        { key: 'NET_AMT_TRADE', label: 'Net Amount Trade', sorter: true, filter: true },
        { key: 'BROKER_COMMS', label: 'Broker Commissions', sorter: true, filter: true },
        { key: 'PROF_LOSS_SEC_CCY', label: 'Profit/Loss', sorter: true, filter: true },
      ],
      overlayModal: false,
      loading: false,
      // columnFilter: true,
      tableFilter: true,
      perPage: 10,
      currentPage: 1,
      totalRecords: 0,
      fromDate: null,
      toDate: null,
      portfolioNumber: null,
      shareSymbol: null,
      securityCurrency: null,

      filterValue: '',
      filteredItems: [],
    };
  },
  methods: {
    async fetchData() {
      this.loading = true;
      console.log(this.fromDate)
      console.log((this.toDate))

      if(this.fromDate == '') {
        this.fromDate = null
      }
      if(this.toDate == '') {
        this.toDate = null
      }
      if(this.portfolioNumber == '') {
        this.portfolioNumber = null
      }
      if(this.shareSymbol == '') {
        this.shareSymbol = null
      }
      if(this.securityCurrency == '') {
        this.securityCurrency = null
      }

      axios.get('http://127.0.0.1:8001/api/combined-transactions', {
        params: {
          from_date: (this.fromDate),
          to_date: (this.toDate),
          portfolio_number: this.portfolioNumber,
          share_symbol: this.shareSymbol,
          security_currency: this.securityCurrency,
        }
      }).then(response => {
        this.items = response.data.records //.map(record => ({ ...record }));
        this.totalRecords = response.data.totalRecords;
        this.loading = false;
        console.log(this.items)
      }).catch(error => {
        console.error("There was an error!", error);
        this.loading = false;
      });
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: '2-digit' };
      return new Date(dateString).toLocaleDateString(undefined, options);
      // return dateString.toLocaleDateString('en-GB', {
      //                                                 day: '2-digit',
      //                                                 month: 'short',
      //                                                 year: 'numeric'
      //                                               });
    },
    formatDateAPI(dateString) {
      if (!dateString) return null;
      const options = { day: '2-digit', month: 'short', year: 'numeric' };
      return new Date(dateString).toLocaleDateString('en-GB', options).replace(/ /g, '-').toUpperCase();
    },
    formatNumber(value) {
      return value.toLocaleString();
    },
    onFilter(value) {
      this.filterValue = value;
      this.filteredItems = this.$refs.dataTable.tableFiltered;
    },
    generatePdf() {
        this.overlayModal = true;
        
        console.log(this.$refs.dataTable.tableFiltered.length);
        // console.log(this.$refs.dataTable.tableFiltered);

        try {
          const pdf = new jsPDF('p', 'pt', 'a4');
          const pdfWidth = pdf.internal.pageSize.getWidth();
          let yOffset = 20;

          // Add PDF Header
          pdf.setFontSize(18);
          pdf.text(`Report`, pdfWidth / 2, yOffset, { align: 'center' });
          yOffset += 30;
          pdf.setFontSize(12);
          pdf.text(`FROM DATE: ${this.fromDate}`, 20, yOffset);
          yOffset += 20;
          pdf.text(`TO DATE: ${this.toDate}`, 20, yOffset);
          yOffset += 20;
          pdf.text(`PORTFOLIO NUMBER: ${this.portfolioNumber}`, 20, yOffset);
          yOffset += 20;
          pdf.text(`SHARE SYMBOL: ${this.shareSymbol}`, 20, yOffset);
          yOffset += 20;
          pdf.text(`SECURITY CURRENCY: ${this.securityCurrency}`, 20, yOffset);
          yOffset += 30;
          pdf.text(`TOTAL RECORDS: ${this.$refs.dataTable.tableFiltered.length}`, 20, yOffset);
          yOffset += 30;

          // Add Table to PDF
          const headers = [
            'TRADE_DATE', 'SECURITY_ACCOUNT', 'SAM_NAME', 'SECURITY_NUMBER',
            'SECURITY_NAME', 'TRANS_TYPE', 'RECID', 'NO_NOMINAL', 'PRICE',
            'NET_AMT_TRADE', 'BROKER_COMMS', 'PROF_LOSS_SEC_CCY'
          ];
          // const tableData = this.items.map(item => headers.map(header => item[header]));
          const tableData = this.$refs.dataTable.tableFiltered.map(item => headers.map(header => item[header]));

          pdf.autoTable({
            startY: yOffset,
            head: [headers],
            body: tableData,
            margin: { top: 10 },
            styles: {fontSize: 6},
          });

          pdf.save('reports.pdf');
          this.overlayModal = false;

        } catch (error) {
          console.error('Error generating PDF:', error);
          this.overlayModal = false;
        }
    },
  },
  mounted() {
    this.fetchData();
  }
}
</script>

<style scoped>
/* Custom styles to set the font size of the CDataTable */
.c-data-table {
  font-size: 12px;
}

/* Set the height of the table container */
.datatable-container {
  min-height: 700px;
  overflow-y: auto;
}
.modal-footer {
  display: none !important;
}
</style>

