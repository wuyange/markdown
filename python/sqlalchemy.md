# sqlalchemy

## 连接数据库

```python
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:123456@10.185.5.86:3306/test", echo=True)
```

1. 数据库URL**:
   这是一个字符串，指定了数据库引擎如何连接到数据库。它的格式通常如下：

   复制

   ```
   dialect+driver://username:password@host:port/database
   ```

   其中各部分的含义如下：

   - `dialect` 是指数据库的种类，如 mysql、postgresql、sqlite 等。
   - `driver` 是数据库连接的驱动程序，如 pymysql、psycopg2、sqlite3 等。这个是可选的，如果不指定，SQLAlchemy会使用默认的驱动程序。
   - `username` 和 `password` 是连接数据库的凭证。
   - `host` 和 `port` 分别是数据库服务器的地址和端口。
   - `database` 是要连接的具体数据库的名称。

   在你的示例中，`mysql+pymysql://root:123456@10.185.5.86:3306/test` 表明使用MySQL数据库，通过PyMySQL驱动程序，以 `root` 用户名和 `123456` 密码连接到位于 `10.185.5.86` 的服务器上的 `3306` 端口上的 `test` 数据库。

2. **echo**:
   `echo` 是一个布尔值，用于设置SQLAlchemy的日志输出。如果设置为 `True`，SQLAlchemy将会记录所有生成的SQL语句和数据库回应的信息，这在调试时非常有用。日志将被输出到Python的标准输出中。在生产环境中，通常将此设置为 `False` 以减少日志噪音和提升性能。

除了这些，`create_engine()` 还可以接受许多其他的参数，用于提供更多的配置选项，比如：

- **pool_size**: 数据库连接池的大小。
- **max_overflow**: 连接池允许的最大溢出连接数。
- **pool_timeout**: 连接池在放弃之前等待连接的秒数。
- **pool_recycle**: 用于设置连接的最大重用时间（以秒为单位），防止数据库长时间不活动而断开连接。
- **isolation_level**: 设置事务的隔离级别。
- **connect_args**: 一个字典，包含传递给数据库连接函数的参数。

## 使用事务的两种方式

```python
fwith engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()
```

在上面的示例中，上下文管理器提供了一个数据库连接，并将操作框定在一个事务中。Python DBAPI 的默认行为包括事务始终在进行中；当连接的作用域被释放时，会发出 ROLLBACK 结束事务。事务不会自动提交；当我们要提交数据时，通常需要调用 `Connection.commit()`

```python
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )
```

我们使用 `Engine.begin()` 方法而不是 `Engine.connect()` 方法来获取连接。该方法既可以管理 `Connection` 的范围，也可以将所有内容都包含在一个事务中，并在结尾处加上 COMMIT（假设成功执行了一个块），或者在出现异常时加上 ROLLBACK。这种方式被称为 begin once

## 获取数据

```python
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
        print(f"x: {row[0]]}  y: {row[1]}")


from sqlalchemy.orm import Session
stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

## 创建数据表

### 方式一

```python
from sqlalchemy import MetaData
metadata_obj = MetaData()
from sqlalchemy import Table, Column, Integer, String, ForeignKey
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(255)),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(255), nullable=False),
)
print(user_table.c.name)
print(user_table.c.keys())
metadata_obj.create_all(engine)
metadata_obj.drop_all(engine)
```

- `Table` - 表示一个数据库表，并将自己分配给一个 `MetaData` 集合。

- `Column` - 表示数据库表中的一列，并将其赋值给 `Table` 对象。 `Column` 通常包括一个字符串名称和一个类型对象。父对象 `Table` 中的 `Column` 对象集合通常通过位于 `Table.c` 的关联数组访问：

  ```
  >>> user_table.c.name
  Column('name', String(length=30), table=<user_account>)
  
  >>> user_table.c.keys()
  ['id', 'name', 'fullname']
  ```

### 方式二

```python
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey, String
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(255))
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(255))
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
Base.metadata.create_all(engine)
```

