function OssUploader(policyUrl, system, user) {
    this.policyUrl = policyUrl;
    this.system = system ? system : 'other';
    this.user = user ? user : 'other';
    this.uploadUrl = '';
    this.expire = 0;
    this.policyBase64 = '';
    this.accessid = '';
    this.signature = '';
    this.host = '';
    this.callbackbody = '';
    this.key = '';
    this.xhr = undefined;
    this.uploadCallback = undefined;
    // http请求
    this.sendRequest = function() {
        if(this.xhr == undefined) {
            if (window.XMLHttpRequest) {
                this.xhr = new XMLHttpRequest();
            } else if (window.ActiveXObject) {
                this.xhr = new ActiveXObject("Microsoft.XMLHTTP");
            } else {
                this.xhr = null;
            }
        }

        if (this.xhr != null) {
            var fd = new FormData();
            fd.append('mode', 'dev');
            fd.append('system', this.system);
            fd.append('user', this.user);
            this.xhr.open("POST", policyUrl, false);
            this.xhr.send(fd);
            return this.xhr.responseText
        } else {
            alert("Your browser does not support XMLHTTP.");
        }
    }
    // 获取上传策略
    this.getSignature = function () {
        //可以判断当前expire是否超过了当前时间,如果超过了当前时间,就重新取一下.3s 做为缓冲
        now = timestamp = Date.parse(new Date()) / 1000;
        if (this.expire < now + 3) {
            console.log('get new sign')
            body = this.sendRequest()
            var res = eval ("(" + body + ")");
            if(res['code'] != '200') {
                alert('获取上传策略失败');
            }
            var obj = res['data'];
            this.host = obj['host']
            this.policyBase64 = obj['policy']
            this.accessid = obj['accessid']
            this.signature = obj['signature']
            this.expire = parseInt(obj['expire'])
            this.callbackbody = obj['callback']
            this.key = obj['dir']
        }
    }
    // 获取新文件名
    this.getNewFileName = function(filename) {
        // eg."Fri, 14 Oct 2016 05:50:03 GMT""
        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
        var randomCode = Math.floor(Math.random() * 9000) + 1000;
        var suffex = filename.split('.').splice(-1);
        var utcTime = new Date().toUTCString();
        var timeArray = utcTime.replace(/(\w+),\s(\d{2})\s(\w+)\s(\d{4})\s(.{8})\s(GMT)/,"$1-$2-$3-$4-$5").split('-')
        var monthIndex = months.indexOf(timeArray[2]);
        var month = new String(monthIndex < 9 ? '0' + (monthIndex + 1) : monthIndex);
        var newFileName = timeArray[3] + month + timeArray[1] + timeArray[4].replace(/\:/g, '') + randomCode;
        return newFileName + '.' + suffex;
    }
    this.upload = function(uploadFile) {
        var self = this;
        this.getSignature();
        var fd = new FormData();
        var key = this.key + this.system + '/' + this.user + '/' + this.getNewFileName(uploadFile.files[0].name);
        fd.append('OSSAccessKeyId', this.accessid);
        fd.append('policy', this.policyBase64);
        fd.append('Signature', this.signature);
        fd.append('success_action_status', '200');
        fd.append('key', key);
        fd.append('callback', this.callbackbody);
        fd.append('file', uploadFile.files[0]);
        this.xhr.upload.addEventListener("progress", function(evt) {
            if (evt.lengthComputable) {
                var percentComplete = Math.round(evt.loaded * 100 / evt.total);
                console.log(percentComplete)
            }
        }, false);
        this.xhr.addEventListener("load", function(evt) {
            if(typeof(self.uploadCallback) == 'function') {
                self.uploadCallback(eval('(' + evt.target.responseText + ')'));
            } else {
                console.log('[INFO] uploadCallback not a function');
            }
        }, false);
        this.xhr.addEventListener("error", function() {
            alert("uoload error");
        }, false);
        this.xhr.addEventListener("abort", function() {
            // alert("已经取消上传");
        }, false);
        this.xhr.open("POST", this.host);
        this.xhr.send(fd);
    }
}