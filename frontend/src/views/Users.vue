<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <CRow>
      <CCol :xs="12">
        <CCard>
          <CCardHeader>
            User Management
            <CButton color="primary" class="float-right" @click="showCreateDialog = true" v-if="isAdmin">
              Create User
            </CButton>
          </CCardHeader>
          <CCardBody>
            <CDataTable
              class="fixed-width-table"
              :items="users"
              :fields="headers"
              :items-per-page="itemsPerPage"
              :active-page="page"
              @update:active-page="page = $event"
              hover
              sorter
              pagination

              :search="search"
              :loading="loading"
              striped
              table-filter
            >
              <template #actions="{ item }">
                <CButton size="sm" color="primary" class="mr-1" @click="editUser(item)">
                  Edit
                </CButton>
                <CButton size="sm" color="danger" class="mr-1" v-if="isAdmin" @click="showDeleteConfirmation(item)">
                  Delete
                </CButton>
              </template>
            </CDataTable>
            <CPagination
              :active-page="page"
              :pages="pageCount"
              @update:active-page="page = $event"
            />
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>

    <CModal
      title="Edit User"
      :show.sync="showEditDialog"
    >
      <CForm @submit.prevent="saveUser" ref="editForm">
        <CInput
          v-model="editedUser.name"
          label="Name"
          :invalid-feedback="rules.required"
          required
        />
        <CInput
          v-model="editedUser.email"
          label="Email"
          type="email"
          readonly
          :invalid-feedback="rules.email"
          required
        />
        <CInput
          v-model="editedUser.address"
          label="Address"
          :invalid-feedback="rules.required"
          required
        />
        <CInput
          v-model="editedUser.contactNumber"
          label="Contact Number"
          :invalid-feedback="rules.required"
          required
        />
        <CButton type="submit" color="success">Save</CButton>
        <CButton color="primary" @click="showEditDialog = false" style="margin-left: 10px;">Cancel</CButton>
        
      </CForm>
      <CAlert v-if="error" color="danger" class="mt-4">
        {{ error }}
      </CAlert>
    </CModal>

    <CModal
      title="Create User"
      :show.sync="showCreateDialog"
    >
      <CForm @submit.prevent="createUser" ref="createForm">
        <CInput
          v-model="newUser.name"
          label="Name"
          :invalid-feedback="rules.required"
          required
        />
        <CInput
          v-model="newUser.email"
          label="Email"
          type="email"
          :invalid-feedback="rules.email"
          required
        />
        <CInput
          v-model="newUser.password"
          label="Password"
          :invalid-feedback="rules.required"
          required
        />
        <CInput
          v-model="newUser.address"
          label="Address"
          :invalid-feedback="rules.required"
          required
        />
        <CInput
          v-model="newUser.contactNumber"
          label="Contact Number"
          :invalid-feedback="rules.required"
          required
        />
        <CButton type="submit" color="success" >Create</CButton>
        <CButton color="primary" @click="showCreateDialog = false" style="margin-left: 10px;">Cancel</CButton>

      </CForm>
      <CAlert v-if="error" color="danger" class="mt-4">
        {{ error }}
      </CAlert>
    </CModal>

    <CModal
      title="Confirm Delete"
      :show.sync="showDeleteDialog"
    >
      <p>Are you sure you want to delete user: {{ userToDelete.name }}?</p>
      <CButton color="danger"  @click="deleteUser">Delete</CButton>
      <CButton color="primary" @click="showDeleteDialog = false" style="margin-left: 10px;">Cancel</CButton>
    </CModal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        { key: 'name', label: 'Name', },
        { key: 'email', label: 'Email',  },
        { key: 'address', label: 'Address',  },
        { key: 'contactNumber', label: 'Contact Number',  },
        { key: 'actions', label: 'Actions',  sortable: false },
      ],
      users: [],
      search: '',
      loading: true,
      page: 1,
      itemsPerPage: 10,
      pageCount: 0,
      showEditDialog: false,
      showCreateDialog:false,
      editedUser: {
        id: null,
        name: '',
        email: '',
        address: '',
        contactNumber: '',
      },
      newUser: {
        name: '',
        email: '',
        password: '',
        address: '',
        contactNumber: '',
      },
      error: null,
      rules: {
        required: 'This field is required.',
        email: 'Invalid email address.',
      },
      showDeleteDialog: false,
      userToDelete: {
        id: null,
        name: '',
        email: '',
        address: '',
        contactNumber: '',
      },
    };
  },
  created() {
    this.fetchUsers();
  },
  computed: {
    isAdmin() {
      return this.$store.state.user && this.$store.state.user.role === 'admin';
    },
  },
  methods: {
    async fetchUsers() {
      try {
        this.loading = true;
        // Fetch users from the backend
        this.users = await this.$store.dispatch('fetchUsers');
      } catch (error) {
        this.error = error.response.data.msg;
      } finally {
        this.loading = false;
      }
    },
    async editUser(user) {
      this.editedUser = {...user };
      this.showEditDialog = true;
    },
    async saveUser() {
      // if (this.$refs.editForm.validate()) 
      {
        try {
          console.log(this.editedUser)
          // Implement edit user logic here
          await this.$store.dispatch('updateUser', this.editedUser);
          this.showEditDialog = false;
          this.fetchUsers();
        } catch (error) {
          this.error = error.response.data.msg;
        }
      }
    },
    showDeleteConfirmation(user) {
      this.userToDelete = user;
      this.showDeleteDialog = true;
    },
    async deleteUser() {
      try {
        // Implement delete user logic here
        await this.$store.dispatch('deleteUser', this.userToDelete.id);
        this.fetchUsers();
        this.showDeleteDialog = false;
      } catch (error) {
        this.error = error.response.data.msg;
      }
    },
    async createUser() {
      // if (this.$refs.createForm.validate()) 
      {
        try {
          // Implement create user logic here
          await this.$store.dispatch('createUser', this.newUser);
          this.showCreateDialog = false;
          this.fetchUsers();
          this.newUser.name = ''
          this.newUser.email = ''
          this.newUser.password = ''
          this.newUser.address = ''
          this.newUser.contactNumber = ''
        } catch (error) {
          this.error = error.response.data.msg;
        }
      }
    },
  },
};
</script>
<style>
  .modal-footer {
    display: none !important;
  }
  .float-right {
    float: right;
  }
  .fixed-width-table {
    table-layout: fixed;
    width: 100%;
  }

  .fixed-width-table th, .fixed-width-table td {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding-top: 10px;
    padding-bottom: 10px;
  }
</style>