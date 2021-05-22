const url = '/articles/'

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';


let startapp = new Vue({
  el: "#startapp",
  delimiters: ['${', '}'],

  data: {
    pageNumber: 0,
    size: 5,
    articles: [],
    loading: false,
    currentArticle: {},
    message: null,
    newArticle: {
      'title': null,
      'category': null,
      'text': '',
      'authors': null,
      'creation_date': null,
      'modified_date': null}
  },

  computed: {
    pageCount() {
      return Math.ceil(this.articles.length / this.size);
    },

    paginatedData() {
      return this.articles.slice(this.pageNumber * this.size, this.pageNumber * this.size + this.size);
    }
  },

  mounted() {
    this.getArticles();
  },

  methods: {
    nextPage() {
      this.pageNumber++;
    },

    prevPage() {
      this.pageNumber--;
    },

    getArticles: function () {
      this.loading = true;
      axios.get(url).then((response) => {
        this.articles = JSON.parse(response.data);
        this.loading = false;
      }).catch((err) => {
        this.loading = false;
        console.log(err)
      })
    },

    getArticle: function (id) {
      this.loading = true;
      axios.get(url + id).then((response) => {
        this.currentArticle = JSON.parse(response.data);

        this.currentArticle = JSON.parse(response.data);
        let authors = [];
        for (let author of this.currentArticle['authors']) {
          authors.push(author.last_name + ' ' + author.first_name + ' ' + author.middle_name);
        }

        this.currentArticle['authors'] = authors.join(', ');

        $("#editArticleModal").modal('show');
        this.loading = false;
      }).catch((err) => {
        this.loading = false;
        console.log(err)
      })
    },

    addArticle: function () {
      this.loading = true;

      let authors = [];
      let authorsSplitted = this.newArticle['authors'].split(', ')
      for (let author of authorsSplitted) {
        let authorSplitted = author.split(' ');
        authors.push({
          'last_name': authorSplitted[0],
          'first_name': authorSplitted[1],
          'middle_name': authorSplitted[2]
        })
      }

      this.newArticle['authors'] = authors

      axios.post(url + 'add', this.newArticle).then((response) => {
        this.loading = false;

        let authors = [];
        for (let author of this.newArticle['authors']) {
          authors.push(author.last_name + ' ' + author.first_name + ' ' + author.middle_name);
        }

        this.newArticle['authors'] = authors.join(', ');

        $("#addArticle").modal('hide');
        this.getArticles();
      }).catch((err) => {
        this.loading = false;
        console.log(err)
      })
    },

    updateArticle: function () {
      this.loading = true;

      let authors = [];
      let authorsSplitted = this.currentArticle['authors'].split(', ')
      for (let author of authorsSplitted) {
        let authorSplitted = author.split(' ');
        authors.push({
          'last_name': authorSplitted[0],
          'first_name': authorSplitted[1],
          'middle_name': authorSplitted[2]
        })
      }

      this.currentArticle['authors'] = authors;

      console.log(this.currentArticle);
      axios.post(url + this.currentArticle.id + '/edit', this.currentArticle).then((response) => {
        this.loading = false;
        this.currentArticle = JSON.parse(response.data);
        let authors = [];
        for (let author of this.currentArticle['authors']) {
          authors.push(author.last_name + ' ' + author.first_name + ' ' + author.middle_name);
        }

        this.currentArticle['authors'] = authors.join(', ');

        this.getArticles();
      }).catch((err) => {
        this.loading = false;
        console.log(err)
      })
    },

    deleteArticle: function (id) {
      this.loading = true;
      axios.delete(url + id + '/delete').then((response) => {
        this.loading = false;
        this.getArticles()
      }).catch((err) => {
        this.loading = false;
        console.log(err)
      })
    }
  },
});