<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol cols="12" sm="8" md="6" lg="4">
          <CCard class="shadow-lg">
            <CCardHeader class="bg-primary text-white text-center">
              <h4>Login</h4>
            </CCardHeader>
            <CCardBody>
              <CForm @submit.prevent="login">
                <CInput
                  v-model="email"
                  type="email"
                  placeholder="Email"
                  aria-label="Email"
                  class="mb-3 form-control-lg"
                  :class="{'is-invalid': !isValid.email && email.length > 0, 'is-valid': isValid.email}"
                  required
                />
                <CInput
                  v-model="password"
                  type="password"
                  placeholder="Password"
                  aria-label="Password"
                  class="mb-3 form-control-lg"
                  :class="{'is-invalid': !isValid.password && password.length > 0, 'is-valid': isValid.password}"
                  required
                />
                <CFormGroup class="d-flex align-items-center mb-3">
                  <CInput
                    v-model="rememberMe"
                    type="checkbox"
                    id="rememberMe"
                  />
                  <CLabel for="rememberMe" class="ml-2 form-check-label">Remember me</CLabel>
                </CFormGroup>
                <CButton type="submit" color="primary" block size="lg">Login</CButton>
              </CForm>
              <CAlert
                color="danger"
                v-if="error"
                class="mt-3"
              >
                {{ error }}
              </CAlert>
            </CCardBody>
            <CCardFooter class="text-center">
              <CButton
                color="link"
                @click="showRegistration"
              >
                Register
              </CButton>
              <CButton
                color="link"
                @click="showForgotPassword"
                class="ml-3"
              >
                Forgot Password
              </CButton>
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
      email: '',
      password: '',
      rememberMe: false,
      error: null,
      isValid: {
        email: false,
        password: false
      },
      emailPattern: /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    };
  },
  methods: {
    async login() {
      if (this.validateForm()) {
        try {
          // Implement JWT authentication logic here
          const token = await this.$store.dispatch('login', {
            email: this.email,
            password: this.password,
          });

          if (token) {
            // Save the token and redirect to the dashboard
            localStorage.setItem('token', token);
            this.$router.push('/dashboard');
          } else {
            this.error = this.$store.getters.errors;
          }
        } catch (error) {
          // Display an error message to the user
          this.error = error.response.data.msg;
        }
      }
    },
    validateForm() {
      this.isValid.email = this.emailPattern.test(this.email);
      this.isValid.password = this.password.length > 0;
      return this.isValid.email && this.isValid.password;
    },
    showRegistration() {
      this.$router.push('/register');
    },
    showForgotPassword() {
      // Implement forgot password logic
    }
  }
};
</script>

<style>
/* Custom styles for modern UI */
body {
  background-color: #f8f9fa;
}
.is-valid {
  border-color: #28a745;
}
.is-invalid {
  border-color: #dc3545;
}
</style>
