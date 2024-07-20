<template>
  <CContainer fluid>
    <CHeader>
      <Navbar></Navbar> 
      <!-- Assuming Navbar is a CoreUI component -->
    </CHeader>

    <CContainer>
      <router-view></router-view>
    </CContainer>

    <CFooter>
      <div>© 2024 My CoreUI App</div>
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