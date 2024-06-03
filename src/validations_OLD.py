import pandas as pd

def validate_dataset(df, tolerance=10e-10):
    prefixes = ['all_types', 'all_res', 'clean_res']
    errors = []

    # Define a helper function to generate column name from one prefix to another
    def get_equivalent_col(col, src_prefix, target_prefix):
        if col.startswith(src_prefix):
            return col.replace(src_prefix, target_prefix)
        return None

    # Check that each all_types is >= all_res and each all_res is >= clean_res
    for i in range(len(prefixes) - 1):
        src_prefix = prefixes[i]
        target_prefix = prefixes[i + 1]

        for col in df.columns:
            if col.startswith(src_prefix):
                target_col = get_equivalent_col(col, src_prefix, target_prefix)
                if target_col in df.columns:
                    # Check for violations considering the tolerance
                    violations_df = df[(df[col] + tolerance) < df[target_col]]
                    if not violations_df.empty:
                        errors.append(f"Validation failed: {col} is not always >= {target_col} within tolerance {tolerance}, "
                                      f"found {len(violations_df)} violations.")

    # Check that build volumes including basement are >= build volumes without basement within each group
    suffix_list = ['_build_vol_FGA_total', '_build_vol']
    inc_basement_suffix_list = ['_build_vol_inc_basement_FGA_total', '_build_vol_inc_basement']
    
    for suffix, inc_basement_suffix in zip(suffix_list,inc_basement_suffix_list ):
        for prefix in prefixes:
            for col in df.columns:
                if col.startswith(prefix) and inc_basement_suffix in col:
                    base_col = col.replace(inc_basement_suffix, suffix)
                    if base_col in df.columns:
                        # Check for violations considering the tolerance
                        violations_df = df[(df[col] + tolerance) < df[base_col]]
                        if not violations_df.empty:
                            errors.append(f"Validation failed: {col} is not always >= {base_col} within tolerance {tolerance}, "
                                        f"found {len(violations_df)} violations.")

    return errors
