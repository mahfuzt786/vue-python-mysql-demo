<template>
 <div class="d-flex justify-content-center align-items-center vh-100">
  <CContainer>
      <CRow class="justify-content-center">
        <CCol xs="12" sm="10" md="8" lg="6">
          <CCard>
            <CCardHeader class="bg-primary text-light">
              <h4 class="mb-0">Register</h4>
            </CCardHeader>
            <CCardBody>
              <CForm @submit.prevent="register">
                <CInput
                  id="name"
                  v-model="name"
                  type="text"
                  placeholder="Enter your name"
                  class="mb-3"
                  :invalid="errors.name !== ''"
                  required
                />

                <CInput
                  id="email"
                  v-model="email"
                  type="email"
                  placeholder="Enter your email"
                  class="mb-3"
                  :invalid="errors.email !== ''"
                  required
                />

                <CInput
                  id="address"
                  v-model="address"
                  type="text"
                  placeholder="Enter your address"
                  class="mb-3"
                  :invalid="errors.address !== ''"
                  required
                />

                <CInput
                  id="password"
                  v-model="password"
                  type="password"
                  placeholder="Enter your password"
                  class="mb-3"
                  :invalid="errors.password !== ''"
                  required
                />

                <CInput
                  id="contactNumber"
                  v-model="contactNumber"
                  type="text"
                  placeholder="Enter your contact number"
                  class="mb-3"
                  :invalid="errors.contactNumber !== ''"
                  required
                />

                <CButton color="primary" type="submit" block>Register</CButton>
              </CForm>
              <CAlert color="danger" class="mt-4" v-if="error">
                {{ error }}
              </CAlert>
              <CAlert color="success" class="mt-4" v-if="success">
                {{ success }}
              </CAlert>
            </CCardBody>
            <CCardFooter class="text-center">
              <CButton color="link" @click="$router.push('/login')">Back to Login</CButton>
            </CCardFooter>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      email: '',
      address: '',
      password: '',
      contactNumber: '',
      error: null,
      success: null,
      errors: {
        name: '',
        email: '',
        address: '',
        password: '',
        contactNumber: '',
      },
    };
  },
  methods: {
    async register() {
      // Clear previous errors
      this.errors = {};

      // Basic validation
      let hasError = false;
      if (!this.name) {
        this.errors.name = 'Name is required.';
        hasError = true;
      }
      if (!this.email) {
        this.errors.email = 'Email is required.';
        hasError = true;
      } else {
        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (!pattern.test(this.email)) {
          this.errors.email = 'Invalid email address.';
          hasError = true;
        }
      }
      if (!this.address) {
        this.errors.address = 'Address is required.';
        hasError = true;
      }
      if (!this.password) {
        this.errors.password = 'Password is required.';
        hasError = true;
      }
      if (!this.contactNumber) {
        this.errors.contactNumber = 'Contact number is required.';
        hasError = true;
      }

      if (hasError) {
        this.error = this.errors;
        return;
      }

      try {
        // Implement registration logic here
        const result = await this.$store.dispatch('register', {
          name: this.name,
          email: this.email,
          address: this.address,
          password: this.password,
          contactNumber: this.contactNumber,
        });

        if (result) {
          this.success = 'Registration successful!';
          setTimeout(() => this.$router.push('/login'), 500);
        } else {
          this.error = 'Registration failed. Please try again.';
        }
      } catch (error) {
        this.error = error.response?.data?.msg || 'An error occurred.';
      }
    },
  },
};
</script>

<style>
  /* Custom styles */

  .CCard {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .CInput.is-invalid {
    border-color: #dc3545;
  }

  .CFormFeedback {
    display: block;
    color: #dc3545;
  }
</style>
