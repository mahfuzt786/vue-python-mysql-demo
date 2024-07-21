<template>
  <!-- <div>
    <CNavbar expand="lg" color-scheme="light" color="black">
      <CNavbarBrand href="#">My Demo App</CNavbarBrand>
      <CToggler @click="drawer = !drawer" v-if="isAuthenticated" />
      <CCollapse :visible="drawer" navbar>
        <CNavbarNav>
          <CNavItem :active="$route.path === '/dashboard'">
            <CLink :href="'/dashboard'">
              <CIcon name="cil-home" /> Home
            </CLink>
          </CNavItem>
          <CNavItem :active="$route.path === '/users'">
            <CLink :href="'/users'">
              <CIcon name="cil-account-multiple" /> Users
            </CLink>
          </CNavItem>
        </CNavbarNav>
        <CNavbarNav class="ml-auto">
          <CNavItem v-if="isAuthenticated">
            <CLink @click="logout">
              <CIcon name="cil-logout" /> Logout
            </CLink>
          </CNavItem>
        </CNavbarNav>
      </CCollapse>
    </CNavbar>
  </div> -->
      <CNavbar expand="lg" type="dark" color="success" style="width: 100%;">
        <CToggler in-navbar @click="collapsed = !collapsed"/>
        <CNavbarBrand href="/">My Demo App</CNavbarBrand>
        <CCollapse :show="collapsed" navbar>
          <CNavbarNav v-if="isAuthenticated">
            <CNavItem v-for="item in menuItems" :key="item.title" :to="item.route" class="menuLinks">
                <CIcon :name="item.icon" />
                {{ item.title }}
            </CNavItem>
          </CNavbarNav>

          
          <CNavbarNav class="ml-auto">
            <CNavItem v-if="isAuthenticated">
              <CLink @click="logout" class="menuLinks">
                <CIcon name="cil-logout" /> Logout
              </CLink>
            </CNavItem>
          </CNavbarNav>
        </CCollapse>
      </CNavbar>
  </template>
  
  <script>
  import { mapGetters } from 'vuex';
  
  export default {    
    computed: {
      ...mapGetters(['isAuthenticated']),
    },
    created() {
      if (!this.$store.getters.isAuthenticated) {
        this.logout();
      }
    },
    data() {
      return {
        drawer: false,
        collapsed: false,
        menuItems: [
          { title: 'Home', icon: 'cil-home', route: '/dashboard' },
          { title: 'Users', icon: 'cil-user', route: '/users' }, // Fixed icon name
        ],
      };
    },
    methods: {
      logout() {
        // Implement logout logic here
        localStorage.removeItem('token');
        this.$store.commit('setToken', '');
        this.$router.push('/login');
      },
    },
  };
  </script>
  
  <style>
  /* Custom styles */
  .menuLinks {
    color: #FFF !important;
    font-weight: bold !important;
    text-decoration: none !important;
  }
  </style>
  