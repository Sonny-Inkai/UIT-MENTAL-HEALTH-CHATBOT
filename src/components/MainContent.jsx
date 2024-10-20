import React from 'react';
import SearchForm from './SearchForm';

function MainContent() {
  return (
    <main id="main" className="clearfix main" role="main">
      <div className="container">
        <div id="main-content" className="row main-content">
          <div id="sidebar-first" className="sidebar span3 site-sidebar-first">
            <div className="row-fluid">
              <div className="region region-sidebar-first clearfix">
                <SearchForm />
              </div>
            </div>
          </div>
          {/* Nội dung chính sẽ nằm ở đây */}
          <div className="content span9">
            {/* Ví dụ về phần nội dung */}
            <h2>Thông báo nổi bật</h2>
            <ul>
              <li><a href="/thong-bao-ky-thi-olympic">Thông báo kỳ thi Olympic</a></li>
              <li><a href="/thong-bao-ve-buoi-tu-van">Thông báo về buổi tư vấn tuyển sinh</a></li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  );
}

export default MainContent;
