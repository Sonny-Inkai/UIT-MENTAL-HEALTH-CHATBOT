import React from 'react';

function Header() {
  return (
    <header className="clearfix header" role="banner">
      <div className="container">
        <div className="row">
          <div className="header-section span12">
            <div id="logo" className="site-logo">
              <a href="/" title="Trang chủ" rel="home">
                <img src="https://student.uit.edu.vn/sites/daa/files/banner.png" alt="Logo UIT" role="presentation" />
              </a>
            </div>
            <div id="site" className="hide">
              <div id="name">
                <a href="/">Cổng thông tin đào tạo</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
