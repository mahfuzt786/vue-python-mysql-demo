<template>
  <CContainer fluid>
    <CHeader>
      <Navbar></Navbar> 
      <!-- Assuming Navbar is a CoreUI component -->
    </CHeader>

    <CWrapper>
      <CRow>
        <CCol xs="12" md="12">
            <router-view></router-view>
      </CCol>
    </CRow>
    </CWrapper>

    <CFooter>
      <div>© 2024 CoreUI App</div>
    </CFooter>
  </CContainer>
</template>

<script>
  import Navbar from './components/Navbar.vue';

  export default {
    name: 'App',

    components: {
      Navbar,
    },

    data: () => ({
      //
    }),
  };

</script>