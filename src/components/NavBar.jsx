import React from 'react';
import '../CSS/NarBar.css';

function NavBar() {
  return (
    <nav id="main-nav" className="clearfix site-main-menu" role="navigation">
      <div className="container">
        <div className="navbar">
          <div className="navbar-inner">
            <button
              aria-label="Navigation menu"
              className="btn btn-navbar collapsed"
              data-toggle="collapse"
              data-target=".nav-collapse"
            >
              <span className="hide">Navigation menu</span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
            </button>
            <div className="nav-collapse collapse">
              <ul className="menu nav">
                <li className="first leaf">
                  <a href="/" title="" className="active">Home</a>
                </li>
                <li className="expanded dropdown">
                  <a href="/gioi-thieu" title="Giới thiệu" className="dropdown-toggle" data-toggle="dropdown">
                    Giới thiệu <span className="caret"></span>
                  </a>
                  <ul className="dropdown-menu">
                    <li><a href="/content/cong-thong-tin-dao-tao">Cổng thông tin đào tạo</a></li>
                    <li><a href="/content/cac-nganh-dao-tao">Các ngành đào tạo</a></li>
                    <li><a href="/content/chuc-nang-nhiem-vu-cua-phong-dao-tao-dai-hoc">Phòng đào tạo đại học</a></li>
                  </ul>
                </li>
                {/* Thêm các mục khác tương tự */}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
