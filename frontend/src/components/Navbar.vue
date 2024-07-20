<template>
    <!-- <div> -->
      <!-- Header -->
      <!-- <CHeader class="bg-primary text-light">
        <CHeaderBrand href="/" class="text-light">
            My Demo App
        </CHeaderBrand>
        <CHeaderNav class="d-md-down-none">
          <CHeaderNavItem v-for="item in menuItems" :key="item.title" :to="item.route">
            <CHeaderNavLink>
              <CIcon :name="item.icon" />
              {{ item.title }}
            </CHeaderNavLink>
          </CHeaderNavItem>
        </CHeaderNav>
        <CButton
          class="d-md-down-none"
          @click="drawer = !drawer"
          v-if="isAuthenticated"
          color="secondary"
        >
          <CIcon name="cil-menu" /> 
        </CButton>
        <CHeaderNavItem>
          <CButton
            color="primary"
            @click="logout"
            v-if="isAuthenticated"
          >
            <CIcon name="cil-account-logout" /> Logout
          </CButton>
        </CHeaderNavItem>
      </CHeader> -->
      
      <!-- Sidebar -->
      <!-- <CSidebar v-model="drawer" show>
        <CSidebarBrand>
          My Demo App
        </CSidebarBrand>
        <CSidebarNav>
          <CNavItem v-for="item in menuItems" :key="item.title" :to="item.route">
            <CIcon :name="item.icon" />
            {{ item.title }}
          </CNavItem>
        </CSidebarNav>
      </CSidebar> 
      <div> -->

      <CNavbar expandable="xl" type="dark" color="black" style="width: 100%;">
    <CToggler in-navbar @click="collapsed = !collapsed"/>
    <CNavbarBrand href="#">NavBar</CNavbarBrand>
    <CCollapse :show="collapsed" navbar>
      <CNavbarNav>
        <CNavItem v-for="item in menuItems" :key="item.title" :href="item.route" >
            <CIcon :name="item.icon" />
            {{ item.title }}
          </CNavItem>

        <CNavItem href="#">Link</CNavItem>
        <CNavItem href="#" disabled>Disabled</CNavItem>
      </CNavbarNav>

      <!-- Right aligned nav items -->
      <CNavbarNav class="ml-auto" style="color: #FFF; font-weight: bold; font-size: 1.2em;">
        

        <CDropdown
          togglerText="Lang"
          nav
          placement="bottom-end"
        >
            <CDropdownItem>EN</CDropdownItem>
            <CDropdownItem>ES</CDropdownItem>
            <CDropdownItem>RU</CDropdownItem>
            <CDropdownItem>FA</CDropdownItem>
        </CDropdown>
        
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
        drawer: true,
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
  body {
    background-color: #f8f9fa;
  }
  </style>
  