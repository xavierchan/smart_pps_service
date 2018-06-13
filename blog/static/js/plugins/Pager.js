/**
 * Created by liying on 2018/6/12.
 */



class Pagination extends React.Component {
  state = {
    data: [],
      blog: {},
  };

  componentDidMount() {
    this.fetchList();
  }

  fetchList () {
      const that = this;
    $.ajax({
        url: '/api/articles',
        type: 'GET',
        success: function (res) {
            if (res.code === 0) {
                that.setState({ data: res.data });
            } else {
                console.log('获取失败');
            }
        }
    });
  }

  fetchDetail (id) {
          const that = this;
        $.ajax({
            url: '/api/articles/' + id,
            type: 'GET',
            success: function (res) {
                that.setState({
                    blog: res
                });
                mdEditor.setMarkdown(res.content);
{#                    if (res.code === 0) {#}
{#                        $('#title').val(res.data.title);#}
{#                        mdEditor.markdown = res.data.content;#}
{#                    } else {#}
{#                        console.log('获取失败');#}
{#                    }#}
            }
        });
    }


  render() {
    const state = this.state;
    return (
        <antd.Pagination showSizeChanger onShowSizeChange={onShowSizeChange} defaultCurrent={3} total={500} />
    );
  }
}



module.exports =

ReactDOM.render(

, mountNode);