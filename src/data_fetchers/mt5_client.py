"""""
MetaTrader 5 数据客户端
"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAU"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass
"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str)"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            #"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            #"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.b"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol ="""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m":"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIM"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w":"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w": mt5.TIMEFRAME_W1,
                "1mo": mt5.TIM"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w": mt5.TIMEFRAME_W1,
                "1mo": mt5.TIMEFRAME_MN1,
            }

            mt5_timeframe = tf_map"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w": mt5.TIMEFRAME_W1,
                "1mo": mt5.TIMEFRAME_MN1,
            }

            mt5_timeframe = tf_map.get(timeframe.lower(), mt5.TIMEF"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w": mt5.TIMEFRAME_W1,
                "1mo": mt5.TIMEFRAME_MN1,
            }

            mt5_timeframe = tf_map.get(timeframe.lower(), mt5.TIMEFRAME_D1)

            #"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w": mt5.TIMEFRAME_W1,
                "1mo": mt5.TIMEFRAME_MN1,
            }

            mt5_timeframe = tf_map.get(timeframe.lower(), mt5.TIMEFRAME_D1)

            # 获取数据
            rates = mt5.copy_rates"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w": mt5.TIMEFRAME_W1,
                "1mo": mt5.TIMEFRAME_MN1,
            }

            mt5_timeframe = tf_map.get(timeframe.lower(), mt5.TIMEFRAME_D1)

            # 获取数据
            rates = mt5.copy_rates_from_pos(mt5_symbol, mt5_timeframe, 0, count)

            if rates is None or len(rates) =="""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w": mt5.TIMEFRAME_W1,
                "1mo": mt5.TIMEFRAME_MN1,
            }

            mt5_timeframe = tf_map.get(timeframe.lower(), mt5.TIMEFRAME_D1)

            # 获取数据
            rates = mt5.copy_rates_from_pos(mt5_symbol, mt5_timeframe, 0, count)

            if rates is None or len(rates) == 0:
                raise DataFetchError(f""""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w": mt5.TIMEFRAME_W1,
                "1mo": mt5.TIMEFRAME_MN1,
            }

            mt5_timeframe = tf_map.get(timeframe.lower(), mt5.TIMEFRAME_D1)

            # 获取数据
            rates = mt5.copy_rates_from_pos(mt5_symbol, mt5_timeframe, 0, count)

            if rates is None or len(rates) == 0:
                raise DataFetchError(f"MT5 无法获取 {mt5_symbol} 的 K 线数据")

"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w": mt5.TIMEFRAME_W1,
                "1mo": mt5.TIMEFRAME_MN1,
            }

            mt5_timeframe = tf_map.get(timeframe.lower(), mt5.TIMEFRAME_D1)

            # 获取数据
            rates = mt5.copy_rates_from_pos(mt5_symbol, mt5_timeframe, 0, count)

            if rates is None or len(rates) == 0:
                raise DataFetchError(f"MT5 无法获取 {mt5_symbol} 的 K 线数据")

            # 转换为 DataFrame
            df = pd"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w": mt5.TIMEFRAME_W1,
                "1mo": mt5.TIMEFRAME_MN1,
            }

            mt5_timeframe = tf_map.get(timeframe.lower(), mt5.TIMEFRAME_D1)

            # 获取数据
            rates = mt5.copy_rates_from_pos(mt5_symbol, mt5_timeframe, 0, count)

            if rates is None or len(rates) == 0:
                raise DataFetchError(f"MT5 无法获取 {mt5_symbol} 的 K 线数据")

            # 转换为 DataFrame
            df = pd.DataFrame(rates)
            df['time"""
MetaTrader 5 数据客户端
需要本地运行 MT5 终端
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import pandas as pd
from loguru import logger

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

from ..utils.exceptions import DataFetchError, ValidationError


class MT5Client:
    """MetaTrader 5 数据客户端"""

    # MT5 品种映射
    SYMBOL_MAP = {
        "xauusd": "XAUUSD",  # 现货黄金
        "xagusd": "XAGUSD",  # 现货白银
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)
        self.config = config

        if not MT5_AVAILABLE:
            raise ImportError("MetaTrader5 模块未安装，请运行: pip install MetaTrader5")

        # 初始化 MT5 连接
        if not mt5.initialize():
            error = mt5.last_error()
            raise DataFetchError(f"MT5 初始化失败: {error}")

        self.logger.info("MT5 客户端初始化成功")

    def __del__(self):
        """析构时关闭 MT5 连接"""
        try:
            mt5.shutdown()
            self.logger.info("MT5 连接已关闭")
        except:
            pass

    def _get_mt5_symbol(self, symbol: str) -> str:
        """转换品种代码为 MT5 格式"""
        return self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 获取品种信息
            symbol_info = mt5.symbol_info(mt5_symbol)
            if symbol_info is None:
                raise DataFetchError(f"MT5 无法获取品种 {mt5_symbol} 信息")

            # 确保数据是最新的
            if not symbol_info.visible:
                if not mt5.symbol_select(mt5_symbol, True):
                    raise DataFetchError(f"MT5 无法选择品种 {mt5_symbol}")

            quote_data = {
                "symbol": symbol,
                "price": float(symbol_info.last),
                "bid": float(symbol_info.bid),
                "ask": float(symbol_info.ask),
                "change": float(symbol_info.last - symbol_info.prev_close),
                "change_percent": float((symbol_info.last - symbol_info.prev_close) / symbol_info.prev_close * 100),
                "high": float(symbol_info.high),
                "low": float(symbol_info.low),
                "open": float(symbol_info.open),
                "volume": float(symbol_info.volume),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"MT5 报价获取成功 {mt5_symbol}: Bid=${quote_data['bid']:.2f}, Ask=${quote_data['ask']:.2f}")
            return quote_data

        except Exception as e:
            raise DataFetchError(f"MT5 获取报价失败: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: int = 200,
    ) -> pd.DataFrame:
        """获取 K 线数据"""
        try:
            mt5_symbol = self._get_mt5_symbol(symbol)

            # 转换时间周期
            tf_map = {
                "1m": mt5.TIMEFRAME_M1,
                "5m": mt5.TIMEFRAME_M5,
                "15m": mt5.TIMEFRAME_M15,
                "30m": mt5.TIMEFRAME_M30,
                "1h": mt5.TIMEFRAME_H1,
                "4h": mt5.TIMEFRAME_H4,
                "1d": mt5.TIMEFRAME_D1,
                "1w": mt5.TIMEFRAME_W1,
                "1mo": mt5.TIMEFRAME_MN1,
            }

            mt5_timeframe = tf_map.get(timeframe.lower(), mt5.TIMEFRAME_D1)

            # 获取数据
            rates = mt5.copy_rates_from_pos(mt5_symbol, mt5_timeframe, 0, count)

            if rates is None or len(rates) == 0:
                raise DataFetchError(f"MT5 无法获取 {mt5_symbol} 的 K 线数据")

            # 转换为 DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit